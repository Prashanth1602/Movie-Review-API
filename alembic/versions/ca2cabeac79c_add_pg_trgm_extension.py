"""add pg_trgm extension

Revision ID: ca2cabeac79c
Revises: ce3679ce8e82
Create Date: 2026-02-18 13:56:37.117390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2cabeac79c'
down_revision: Union[str, None] = 'ce3679ce8e82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
