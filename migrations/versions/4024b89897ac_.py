"""empty message

Revision ID: 4024b89897ac
Revises: 2a2838cab69c
Create Date: 2022-07-30 17:44:26.786470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4024b89897ac'
down_revision = '2a2838cab69c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('availabilities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('day_possible', sa.String(length=32), nullable=True),
    sa.Column('availability_owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['availability_owner'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('availabilities')
    # ### end Alembic commands ###