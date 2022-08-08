"""empty message

Revision ID: 8593d6cac36a
Revises: 248f0815022b
Create Date: 2022-07-31 19:57:58.475734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8593d6cac36a'
down_revision = '248f0815022b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subjects_grades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subject', sa.String(length=32), nullable=True),
    sa.Column('grade_from', sa.String(length=32), nullable=True),
    sa.Column('grade_to', sa.String(length=32), nullable=True),
    sa.Column('user_subjects_owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_subjects_owner'], ['tutoring.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('subjects_user_subjects_owner_fkey', 'subjects', type_='foreignkey')
    op.drop_column('subjects', 'user_subjects_owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('user_subjects_owner', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('subjects_user_subjects_owner_fkey', 'subjects', 'tutoring', ['user_subjects_owner'], ['id'])
    op.drop_table('subjects_grades')
    # ### end Alembic commands ###