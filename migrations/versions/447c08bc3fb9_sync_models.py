"""sync-models

Revision ID: 447c08bc3fb9
Revises: 7a6df1e9fdfe
Create Date: 2025-05-14 21:12:41.401901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '447c08bc3fb9'
down_revision: Union[str, None] = '7a6df1e9fdfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
