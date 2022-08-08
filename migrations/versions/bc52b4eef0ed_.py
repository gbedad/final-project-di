"""empty message

Revision ID: bc52b4eef0ed
Revises: 3dbc01e38474
Create Date: 2022-08-04 16:37:42.730499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc52b4eef0ed'
down_revision = '3dbc01e38474'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('course_student_fkey', 'course', type_='foreignkey')
    op.drop_constraint('course_tutor_fkey', 'course', type_='foreignkey')
    op.create_foreign_key(None, 'course', 'course', ['student'], ['id'])
    op.create_foreign_key(None, 'course', 'course', ['tutor'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.create_foreign_key('course_tutor_fkey', 'course', 'user', ['tutor'], ['id'])
    op.create_foreign_key('course_student_fkey', 'course', 'students', ['student'], ['id'])
    # ### end Alembic commands ###