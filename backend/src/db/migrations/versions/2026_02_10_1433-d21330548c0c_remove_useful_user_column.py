"""remove useful user column.

Revision ID: d21330548c0c
Revises: 681fc56cba9a
Create Date: 2026-02-10 14:33:44.032785

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "d21330548c0c"
down_revision = "681fc56cba9a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Run the migration."""
    op.drop_column("users", "is_profile_completed")


def downgrade() -> None:
    """Undo the migration."""
    op.add_column(
        "users",
        sa.Column(
            "is_profile_completed",
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=False,
        ),
    )
