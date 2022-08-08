"""empty message

Revision ID: 96c427d4aa87
Revises: 5b85ed88dbc2
Create Date: 2022-07-22 10:03:43.724242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96c427d4aa87'
down_revision = '5b85ed88dbc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('more_about_me', sa.Column('inquiry', sa.String(length=32), nullable=True))
    op.drop_column('more_about_me', 'how')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('more_about_me', sa.Column('how', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_column('more_about_me', 'inquiry')
    # ### end Alembic commands ###