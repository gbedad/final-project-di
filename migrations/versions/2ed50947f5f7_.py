"""empty message

Revision ID: 2ed50947f5f7
Revises: 4024b89897ac
Create Date: 2022-07-30 17:45:58.968584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ed50947f5f7'
down_revision = '4024b89897ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('availabilities', sa.Column('day_time_from', sa.String(length=32), nullable=True))
    op.add_column('availabilities', sa.Column('day_time_to', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('availabilities', 'day_time_to')
    op.drop_column('availabilities', 'day_time_from')
    # ### end Alembic commands ###
