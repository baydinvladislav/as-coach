"""gender and user field

Revision ID: da7d9ec115c8
Revises: 0774e2e2d227
Create Date: 2023-03-31 20:30:31.061985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da7d9ec115c8'
down_revision = '0774e2e2d227'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customer', 'gender',
               existing_type=postgresql.ENUM('MALE', 'FEMALE', name='gender'),
               nullable=True)
    op.alter_column('customer', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customer', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('customer', 'gender',
               existing_type=postgresql.ENUM('MALE', 'FEMALE', name='gender'),
               nullable=False)
    # ### end Alembic commands ###
