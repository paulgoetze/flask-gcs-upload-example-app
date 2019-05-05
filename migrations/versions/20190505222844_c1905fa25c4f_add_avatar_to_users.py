"""add_avatar_to_users

Revision ID: c1905fa25c4f
Revises: 5b5edadb5f5f
Create Date: 2019-05-05 22:28:44.002663

"""
import sqlalchemy as sa
from alembic import op

from depot.fields.sqlalchemy import UploadedFileField

# revision identifiers, used by Alembic.
revision = 'c1905fa25c4f'
down_revision = '5b5edadb5f5f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('avatar', UploadedFileField(), nullable=True))


def downgrade():
    op.drop_column('users', 'avatar')
