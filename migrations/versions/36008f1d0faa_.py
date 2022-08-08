"""empty message

Revision ID: 36008f1d0faa
Revises: 01b5afd9777e
Create Date: 2022-07-27 22:01:29.043184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36008f1d0faa'
down_revision = '01b5afd9777e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interviews', sa.Column('interview_time', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interviews', 'interview_time')
    # ### end Alembic commands ###