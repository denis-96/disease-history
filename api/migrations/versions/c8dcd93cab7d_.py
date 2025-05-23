"""empty message

Revision ID: c8dcd93cab7d
Revises: 
Create Date: 2023-05-21 17:44:00.671092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8dcd93cab7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rubric_sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('auth_refresh_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('diagnosis', sa.String(), nullable=True),
    sa.Column('complaints', sa.String(), nullable=True),
    sa.Column('anamnesis', sa.String(), nullable=True),
    sa.Column('heredity', sa.String(), nullable=True),
    sa.Column('treatment_plan', sa.String(), nullable=True),
    sa.Column('treatment_comments', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rubrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['rubric_sections.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treatment_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rubrics_variants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rubric_id', sa.Integer(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['treatment_records.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['rubric_id'], ['rubrics.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rubric_id', 'record_id', name='rub_id_rec_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rubrics_variants')
    op.drop_table('treatment_records')
    op.drop_table('rubrics')
    op.drop_table('patients')
    op.drop_table('auth_refresh_tokens')
    op.drop_table('users')
    op.drop_table('rubric_sections')
    # ### end Alembic commands ###
