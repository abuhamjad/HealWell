"""refine_user_profile

Revision ID: 003
Revises: 002
Create Date: 2026-07-25 15:30:00.000000

Remove age column (replaced by calculated age from date_of_birth).
Add preferred_name column for display name throughout the application.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove age column and add preferred_name column."""
    # Drop age column (replaced by date_of_birth as source of truth)
    op.drop_column("users", "age")

    # Add preferred_name column for display name
    op.add_column("users", sa.Column("preferred_name", sa.String(100), nullable=True))


def downgrade() -> None:
    """Restore age column and remove preferred_name column."""
    # Remove preferred_name column
    op.drop_column("users", "preferred_name")

    # Restore age column
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))
