"""sukurta car ir defect lenteles

Revision ID: 3c9196ca4cf9
Revises: 81e7801512b8
Create Date: 2022-02-23 21:51:42.453768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c9196ca4cf9'
down_revision = '81e7801512b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('defect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('price', sa.String(length=300), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('car', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'car', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'car', type_='foreignkey')
    op.drop_column('car', 'user_id')
    op.drop_table('defect')
    # ### end Alembic commands ###
