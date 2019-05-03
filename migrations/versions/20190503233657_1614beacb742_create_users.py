"""create_users

Revision ID: 1614beacb742
Revises:
Create Date: 2019-05-03 23:36:57.798125

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '1614beacb742'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
