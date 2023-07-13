"""empty message

Revision ID: 853b83c96cce
Revises: 0d07db7f2aac
Create Date: 2023-07-13 02:19:10.123461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '853b83c96cce'
down_revision = '0d07db7f2aac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('gravity')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gravity', sa.VARCHAR(length=250), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
