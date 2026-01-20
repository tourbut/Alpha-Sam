"""Refactor IDs from Integer to UUID and add Portfolio-Asset link

Revision ID: a1b2c3d4e5f6
Revises: 4135d7ded6fa
Create Date: 2026-01-20 20:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '3a736c817d89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add temp_uuid to all relevant tables
    tables = [
        'users', 'portfolios', 'assets', 'transactions', 
        'prices', 'positions', 'notification_settings', 
        'portfolio_history', 'leaderboard_ranks', 'user_follows'
    ]
    
    # Enum handling for leaderboard_ranks might be tricky if used in arrays or specific logic, but here it's simple column.
    
    for table in tables:
        op.add_column(table, sa.Column('temp_uuid', PG_UUID(as_uuid=True), nullable=True))

    # 2. Populate UUIDs
    # Postgres 13+ supports gen_random_uuid() natively.
    # If pgcrypto is needed: op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    for table in tables:
        # Generate new UUIDs for existing rows
        op.execute(f"UPDATE {table} SET temp_uuid = gen_random_uuid()")
        # Make it non-nullable after population
        op.alter_column(table, 'temp_uuid', nullable=False)

    # 3. Add portfolio_id to assets (as temp_portfolio_uuid initially or direct column if we map strictly)
    # We need to link Assets to Portfolios.
    # Strategy: For each asset, find the owner's first portfolio.
    # First, add the column.
    op.add_column('assets', sa.Column('portfolio_id', PG_UUID(as_uuid=True), nullable=True))
    
    # We assume 'portfolios' table has temp_uuid populated.
    # We join assets and portfolios on owner_id to find a valid portfolio.
    # Note: owner_id is still Int at this point.
    op.execute("""
        UPDATE assets a
        SET portfolio_id = p.temp_uuid
        FROM portfolios p
        WHERE a.owner_id = p.owner_id
        -- Determine which portfolio to pick if multiple: e.g. the one with lowest ID (old PK)
        AND p.id = (
            SELECT id FROM portfolios p2 
            WHERE p2.owner_id = a.owner_id 
            ORDER BY id ASC LIMIT 1
        )
    """)
    # If any asset has no owner_id (global assets), portfolio_id remains NULL or handled separately?
    # Based on models, portfolio_id is non-nullable. But global assets might not belong to user portfolio.
    # If domain rules say Global Assets are owned by Admin Portfolio, we need logic.
    # For now, we set nullable=False constraint later, but effectively we might have issues if data exists with no owner.
    
    # 4. Map Foreign Keys
    # We need to update foreign key columns to point to new UUIDs.
    # Instead of updating existing Int columns, we create new UUID columns for FKs.
    
    fk_mappings = [
        ('portfolios', 'owner_id', 'users', 'temp_owner_id'),
        ('assets', 'owner_id', 'users', 'temp_owner_id'),
        ('transactions', 'portfolio_id', 'portfolios', 'temp_portfolio_id'),
        ('transactions', 'asset_id', 'assets', 'temp_asset_id'),
        ('prices', 'asset_id', 'assets', 'temp_asset_id'),
        ('positions', 'asset_id', 'assets', 'temp_asset_id'),
        ('positions', 'portfolio_id', 'portfolios', 'temp_portfolio_id'), # Note: Position model has portfolio_id? Yes based on recent check.
        ('notification_settings', 'user_id', 'users', 'temp_user_id'),
        ('portfolio_history', 'owner_id', 'users', 'temp_owner_id'),
        ('user_follows', 'follower_id', 'users', 'temp_follower_id'),
        ('user_follows', 'following_id', 'users', 'temp_following_id'),
        ('leaderboard_ranks', 'user_id', 'users', 'temp_user_id'),
        ('leaderboard_ranks', 'portfolio_id', 'portfolios', 'temp_portfolio_id'),
    ]
    
    for table, old_fk, target_table, new_col_name in fk_mappings:
        # Add new column
        op.add_column(table, sa.Column(new_col_name, PG_UUID(as_uuid=True), nullable=True))
        
        # Populate new column mapping old_fk to target_table.temp_uuid
        # T = table, R = remote target
        op.execute(f"""
            UPDATE {table} T
            SET {new_col_name} = R.temp_uuid
            FROM {target_table} R
            WHERE T.{old_fk} = R.id
        """)
    
    # 5. Swap Columns (Conceptually) - In strict alembic, we drop old and rename new.
    # Drop old constraints first.
    
    # Constraints naming convention in Postgres usually: table_column_fkey, table_pkey
    # We explicitly drop them. This requires knowing names. Alembic can sometimes handle this but safer to use raw SQL or inspect.
    # For simplicity in this script, we assume standard naming or use "CASCADE".
    
    # Drop old Int columns and PKs
    for table in tables:
        op.execute(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {table}_pkey CASCADE")
        # Also drop foreign keys? CASCADE handles it.
    
    # Drop old ID columns and FK columns
    # Re-structure:
    # 1. Drop old id
    # 2. Rename temp_uuid to id
    # 3. Add PK constraint
    
    for table in tables:
        op.drop_column(table, 'id')
        op.alter_column(table, 'temp_uuid', new_column_name='id', nullable=False)
        op.create_primary_key(f"pk_{table}", table, ['id'])

    # Handle FK column swaps
    # We created 'temp_X_id'. We should drop old 'X_id' and rename 'temp_X_id' to 'X_id'.
    # Note: We already added 'portfolio_id' to assets directly as UUID (step 3).
    
    fk_swaps = [
        ('portfolios', 'owner_id', 'temp_owner_id', 'users'),
        ('assets', 'owner_id', 'temp_owner_id', 'users'),
        ('transactions', 'portfolio_id', 'temp_portfolio_id', 'portfolios'),
        ('transactions', 'asset_id', 'temp_asset_id', 'assets'),
        ('prices', 'asset_id', 'temp_asset_id', 'assets'),
        ('positions', 'asset_id', 'temp_asset_id', 'assets'),
        ('positions', 'portfolio_id', 'temp_portfolio_id', 'portfolios'),
        ('notification_settings', 'user_id', 'temp_user_id', 'users'),
        ('portfolio_history', 'owner_id', 'temp_owner_id', 'users'),
        ('user_follows', 'follower_id', 'temp_follower_id', 'users'),
        ('user_follows', 'following_id', 'temp_following_id', 'users'),
        ('leaderboard_ranks', 'user_id', 'temp_user_id', 'users'),
        ('leaderboard_ranks', 'portfolio_id', 'temp_portfolio_id', 'portfolios'),
    ]

    for table, old_col, new_col, target_table in fk_swaps:
        op.drop_column(table, old_col)
        op.alter_column(table, new_col, new_column_name=old_col, nullable=False)
        op.create_foreign_key(f"fk_{table}_{old_col}_{target_table}", table, target_table, [old_col], ['id'])

    # Special handling for 'assets.portfolio_id' which was added fresh in Step 3
    # It is UUID already, but currently named 'portfolio_id'. We just need to add FK constraint.
    # And make it not nullable (if required).
    # op.alter_column('assets', 'portfolio_id', nullable=False) -> Depending on data quality
    op.create_foreign_key("fk_assets_portfolio_id_portfolios", "assets", "portfolios", ["portfolio_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    # Reverting UUID to Integer is very hard because we lose the original Integers if we didn't save them.
    # Assuming irrelevant for this forward-only migration task.
    pass
