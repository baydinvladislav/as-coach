"""add product foreign key

Revision ID: e84676267e77
Revises: 9543c57a9455
Create Date: 2024-08-23 12:11:24.186724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e84676267e77'
down_revision = '9543c57a9455'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('coach_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'product', 'coach', ['coach_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'coach_id')
    # ### end Alembic commands ###
