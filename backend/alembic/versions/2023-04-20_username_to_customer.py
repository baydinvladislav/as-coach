"""username to customer

Revision ID: 86e47c3979ad
Revises: 7db71b08defe
Create Date: 2023-04-20 09:54:35.098796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86e47c3979ad'
down_revision = '7db71b08defe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('username', sa.String(length=100), nullable=True))
    op.drop_column('customer', 'phone_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone_number', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('customer', 'username')
    # ### end Alembic commands ###