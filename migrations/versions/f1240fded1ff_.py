"""empty message

Revision ID: f1240fded1ff
Revises: bc52b4eef0ed
Create Date: 2022-08-04 16:38:42.669353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1240fded1ff'
down_revision = 'bc52b4eef0ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('course_table_course_id_fkey', 'course_table', type_='foreignkey')
    op.drop_column('course_table', 'course_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course_table', sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('course_table_course_id_fkey', 'course_table', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###
