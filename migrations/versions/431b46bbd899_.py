"""empty message

Revision ID: 431b46bbd899
Revises: 7cb79b90def8
Create Date: 2022-08-30 21:52:45.004849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '431b46bbd899'
down_revision = '7cb79b90def8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'course', ['id'])
    op.create_unique_constraint(None, 'tutoring', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tutoring', type_='unique')
    op.drop_constraint(None, 'course', type_='unique')
    # ### end Alembic commands ###
