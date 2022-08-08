"""empty message

Revision ID: 849d4855a70c
Revises: f74ea2ebb313
Create Date: 2022-08-07 13:59:44.360577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '849d4855a70c'
down_revision = 'f74ea2ebb313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interviews', sa.Column('is_done', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interviews', 'is_done')
    # ### end Alembic commands ###