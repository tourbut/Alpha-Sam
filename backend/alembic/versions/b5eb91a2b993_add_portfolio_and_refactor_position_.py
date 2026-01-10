"""Add Portfolio and refactor Position/Transaction

Revision ID: b5eb91a2b993
Revises: 2194c7f4929f
Create Date: 2026-01-10 21:44:55.756746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b5eb91a2b993'
down_revision: Union[str, Sequence[str], None] = '2194c7f4929f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    
    # 1. Create Portfolios table
    op.create_table('portfolios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_owner_id'), 'portfolios', ['owner_id'], unique=False)

    # 2. Add Nullable portfolio_id columns first
    op.add_column('positions', sa.Column('portfolio_id', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('portfolio_id', sa.Integer(), nullable=True))

    # 3. Data Migration: Create Default Portfolio for each User and link data
    # We strictly use SQL for migration to avoid model dependency issues
    users = session.execute(sa.text("SELECT id FROM users")).fetchall()
    
    for user in users:
        user_id = user[0]
        # Create Default Portfolio
        result = session.execute(
            sa.text("INSERT INTO portfolios (owner_id, name, description, currency, created_at, updated_at) VALUES (:uid, '메인 포트폴리오', 'Default Portfolio', 'USD', NOW(), NOW()) RETURNING id"),
            {"uid": user_id}
        )
        portfolio_id = result.scalar()
        
        # Link Positions
        session.execute(
            sa.text("UPDATE positions SET portfolio_id = :pid WHERE owner_id = :uid"),
            {"pid": portfolio_id, "uid": user_id}
        )
        
        # Link Transactions
        session.execute(
            sa.text("UPDATE transactions SET portfolio_id = :pid WHERE owner_id = :uid"),
            {"pid": portfolio_id, "uid": user_id}
        )
    
    session.commit()

    # 4. Enforce Non-Null Constraints now that data is populated
    op.alter_column('positions', 'portfolio_id', nullable=False)
    op.alter_column('transactions', 'portfolio_id', nullable=False)

    # 5. Continue with other schema changes
    op.add_column('positions', sa.Column('avg_price', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('positions', sa.Column('last_transaction_id', sa.Integer(), nullable=True))
    
    # Initialize avg_price from buy_price for migration (best effort)
    session.execute(sa.text("UPDATE positions SET avg_price = buy_price"))
    # Also ensure avg_price is not null if we want (it is nullable=False in model but nullable=True in DB initially?)
    # Model says: ge=0.0 which implies not null usually, but for migration safely keep nullable=True handled below?
    # Schema generated: nullable=True for avg_price. So we are fine.
    
    op.drop_index(op.f('ix_positions_owner_id'), table_name='positions')
    op.drop_constraint(op.f('uq_position_owner_asset'), 'positions', type_='unique')
    op.create_index(op.f('ix_positions_portfolio_id'), 'positions', ['portfolio_id'], unique=False)
    op.create_unique_constraint('uq_position_portfolio_asset', 'positions', ['portfolio_id', 'asset_id'])
    op.drop_constraint(op.f('fk_positions_owner_id_users'), 'positions', type_='foreignkey')
    op.create_foreign_key(None, 'positions', 'transactions', ['last_transaction_id'], ['id'])
    op.create_foreign_key(None, 'positions', 'portfolios', ['portfolio_id'], ['id'])
    
    op.drop_column('positions', 'buy_date')
    op.drop_column('positions', 'owner_id')
    op.drop_column('positions', 'buy_price') # We migrated to avg_price
    
    op.add_column('transactions', sa.Column('executed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('transactions', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    
    # Copy timestamp to executed_at
    session.execute(sa.text("UPDATE transactions SET executed_at = timestamp"))
    
    op.drop_index(op.f('ix_transactions_owner_id'), table_name='transactions')
    op.create_index(op.f('ix_transactions_portfolio_id'), 'transactions', ['portfolio_id'], unique=False)
    op.drop_constraint(op.f('fk_transactions_owner_id_users'), 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'portfolios', ['portfolio_id'], ['id'])
    
    op.drop_column('transactions', 'timestamp')
    op.drop_column('transactions', 'owner_id')


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('timestamp', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key(op.f('fk_transactions_owner_id_users'), 'transactions', 'users', ['owner_id'], ['id'])
    op.drop_index(op.f('ix_transactions_portfolio_id'), table_name='transactions')
    op.create_index(op.f('ix_transactions_owner_id'), 'transactions', ['owner_id'], unique=False)
    op.drop_column('transactions', 'created_at')
    op.drop_column('transactions', 'executed_at')
    op.drop_column('transactions', 'portfolio_id')
    op.add_column('positions', sa.Column('buy_price', sa.NUMERIC(precision=20, scale=8), autoincrement=False, nullable=True))
    op.add_column('positions', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('positions', sa.Column('buy_date', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.create_foreign_key(op.f('fk_positions_owner_id_users'), 'positions', 'users', ['owner_id'], ['id'])
    op.drop_constraint('uq_position_portfolio_asset', 'positions', type_='unique')
    op.drop_index(op.f('ix_positions_portfolio_id'), table_name='positions')
    op.create_unique_constraint(op.f('uq_position_owner_asset'), 'positions', ['owner_id', 'asset_id'], postgresql_nulls_not_distinct=False)
    op.create_index(op.f('ix_positions_owner_id'), 'positions', ['owner_id'], unique=False)
    op.drop_column('positions', 'last_transaction_id')
    op.drop_column('positions', 'avg_price')
    op.drop_column('positions', 'portfolio_id')
    op.drop_index(op.f('ix_portfolios_owner_id'), table_name='portfolios')
    op.drop_table('portfolios')
    # ### end Alembic commands ###
