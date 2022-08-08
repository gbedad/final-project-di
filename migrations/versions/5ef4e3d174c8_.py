"""empty message

Revision ID: 5ef4e3d174c8
Revises: bef75d9db971
Create Date: 2022-08-04 17:04:16.687837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ef4e3d174c8'
down_revision = 'bef75d9db971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('course_tutor_fkey', 'course', type_='foreignkey')
    op.drop_constraint('course_student_fkey', 'course', type_='foreignkey')
    op.create_foreign_key(None, 'course', 'user', ['tutor'], ['id'])
    op.create_foreign_key(None, 'course', 'students', ['student'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.create_foreign_key('course_student_fkey', 'course', 'course', ['student'], ['id'])
    op.create_foreign_key('course_tutor_fkey', 'course', 'course', ['tutor'], ['id'])
    # ### end Alembic commands ###