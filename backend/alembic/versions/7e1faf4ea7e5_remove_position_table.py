"""remove_position_table

Revision ID: 7e1faf4ea7e5
Revises: b5eb91a2b993
Create Date: 2026-01-11 23:58:49.974769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e1faf4ea7e5'
down_revision: Union[str, Sequence[str], None] = 'b5eb91a2b993'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # positions 테이블 삭제
    op.drop_table('positions')


def downgrade() -> None:
    """Downgrade schema."""
    # downgrade 시 positions 테이블 재생성 (데이터는 복원되지 않음)
    op.create_table('positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('avg_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('last_transaction_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['last_transaction_id'], ['transactions.id'], ),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('portfolio_id', 'asset_id', name='uq_position_portfolio_asset')
    )
    op.create_index(op.f('ix_positions_asset_id'), 'positions', ['asset_id'], unique=False)
    op.create_index(op.f('ix_positions_portfolio_id'), 'positions', ['portfolio_id'], unique=False)
