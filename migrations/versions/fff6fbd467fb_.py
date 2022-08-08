"""empty message

Revision ID: fff6fbd467fb
Revises: 975f51cbac11
Create Date: 2022-08-04 20:03:15.334120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff6fbd467fb'
down_revision = '975f51cbac11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_student_course',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], )
    )
    op.drop_column('course', 'subject')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('subject', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_table('association_student_course')
    # ### end Alembic commands ###