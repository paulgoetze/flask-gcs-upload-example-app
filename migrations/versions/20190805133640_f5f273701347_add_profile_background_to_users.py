"""add_profile_background_to_users

Revision ID: f5f273701347
Revises: c1905fa25c4f
Create Date: 2019-08-05 13:36:40.204981

"""
from alembic import op
import sqlalchemy as sa

from depot.fields.sqlalchemy import UploadedFileField

# revision identifiers, used by Alembic.
revision = 'f5f273701347'
down_revision = 'c1905fa25c4f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('profile_background', UploadedFileField(), nullable=True))


def downgrade():
    op.drop_column('users', 'profile_background')
