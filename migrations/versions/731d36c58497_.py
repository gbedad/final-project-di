"""empty message

Revision ID: 731d36c58497
Revises: c568a168211c
Create Date: 2022-10-01 19:34:13.232904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '731d36c58497'
down_revision = 'c568a168211c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upload_b3',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('b3_filename', sa.String(length=100), nullable=True),
    sa.Column('b3_data', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('upload_cv',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cv_filename', sa.String(length=100), nullable=True),
    sa.Column('cv_data', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('upload_id',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_filename', sa.String(length=100), nullable=True),
    sa.Column('id_data', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('upload')
    op.drop_column('tutoring', 'svt')
    op.drop_column('tutoring', 'monday')
    op.drop_column('tutoring', 'wednesday')
    op.drop_column('tutoring', 'english')
    op.drop_column('tutoring', 'geopolitics')
    op.drop_column('tutoring', 'sunday')
    op.drop_column('tutoring', 'tuesday')
    op.drop_column('tutoring', 'maths')
    op.drop_column('tutoring', 'french')
    op.drop_column('tutoring', 'physics')
    op.drop_column('tutoring', 'spanish')
    op.drop_column('tutoring', 'thursday')
    op.drop_column('tutoring', 'friday')
    op.drop_column('tutoring', 'history')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tutoring', sa.Column('history', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('friday', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('thursday', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('spanish', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('physics', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('french', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('maths', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('tuesday', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('sunday', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('geopolitics', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('english', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('wednesday', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('monday', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.add_column('tutoring', sa.Column('svt', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.create_table('upload',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('cv_filename', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('cv_data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('b3_filename', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('b3_data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('id_filename', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('id_data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='upload_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='upload_pkey'),
    sa.UniqueConstraint('user_id', name='upload_user_id_key')
    )
    op.drop_table('upload_id')
    op.drop_table('upload_cv')
    op.drop_table('upload_b3')
    # ### end Alembic commands ###