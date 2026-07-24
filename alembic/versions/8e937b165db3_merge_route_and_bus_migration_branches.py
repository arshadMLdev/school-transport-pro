"""merge route and bus migration branches

Revision ID: 8e937b165db3
Revises: 9f968afd3d51, d6291f0d2ddb
Create Date: 2026-07-24 00:27:42.404990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e937b165db3'
down_revision: Union[str, Sequence[str], None] = ('9f968afd3d51', 'd6291f0d2ddb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
