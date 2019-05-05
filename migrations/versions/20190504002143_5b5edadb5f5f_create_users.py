"""create_users

Revision ID: 5b5edadb5f5f
Revises:
Create Date: 2019-05-04 00:21:43.029010

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5b5edadb5f5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
