"""nutritition models init

Revision ID: 08d8c7b46ca4
Revises: ea88688fea0d
Create Date: 2024-08-17 11:22:42.296119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '08d8c7b46ca4'
down_revision = 'ea88688fea0d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('product_type', sa.Enum('GRAM', 'MILLILITER', 'PORTION', name='producttype'), nullable=False),
    sa.Column('proteins', sa.Integer(), nullable=False),
    sa.Column('fats', sa.Integer(), nullable=False),
    sa.Column('carbs', sa.Integer(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.Column('vendor_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    op.create_table('meal',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('diet_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('total_calories', sa.Integer(), nullable=False),
    sa.Column('consumed_calories', sa.Integer(), nullable=True),
    sa.Column('total_proteins', sa.Integer(), nullable=False),
    sa.Column('consumed_proteins', sa.Integer(), nullable=True),
    sa.Column('total_fats', sa.Integer(), nullable=True),
    sa.Column('consumed_fats', sa.Integer(), nullable=False),
    sa.Column('total_carbs', sa.Integer(), nullable=True),
    sa.Column('consumed_carbs', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['diet_id'], ['diet.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meal_id'), 'meal', ['id'], unique=False)
    op.create_table('productinmeal',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('meal_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_productinmeal_id'), 'productinmeal', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_productinmeal_id'), table_name='productinmeal')
    op.drop_table('productinmeal')
    op.drop_index(op.f('ix_meal_id'), table_name='meal')
    op.drop_table('meal')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###