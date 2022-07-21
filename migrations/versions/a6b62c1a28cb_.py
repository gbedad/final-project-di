"""empty message

Revision ID: a6b62c1a28cb
Revises: 4ac615620bc4
Create Date: 2022-07-21 14:24:43.597920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6b62c1a28cb'
down_revision = '4ac615620bc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_information',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('zipcode', sa.String(length=32), nullable=True),
    sa.Column('email2', sa.String(length=32), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('birth_date', sa.String(length=32), nullable=True),
    sa.Column('short_text', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('my_information')
    # ### end Alembic commands ###
