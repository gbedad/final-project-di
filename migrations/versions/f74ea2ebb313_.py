"""empty message

Revision ID: f74ea2ebb313
Revises: 1446940659c6
Create Date: 2022-08-07 10:16:59.058299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74ea2ebb313'
down_revision = '1446940659c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'upload', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'upload', type_='foreignkey')
    op.drop_column('upload', 'user_id')
    # ### end Alembic commands ###