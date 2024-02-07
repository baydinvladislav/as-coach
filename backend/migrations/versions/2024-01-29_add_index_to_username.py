"""add index to username

Revision ID: ebc6d52a6622
Revises: b266714bcb19
Create Date: 2024-01-29 19:34:10.199816

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebc6d52a6622'
down_revision = 'b266714bcb19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_coach_username'), 'coach', ['username'], unique=False)
    op.create_index(op.f('ix_customer_username'), 'customer', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customer_username'), table_name='customer')
    op.drop_index(op.f('ix_coach_username'), table_name='coach')
    # ### end Alembic commands ###