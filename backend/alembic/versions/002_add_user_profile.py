"""add_user_profile

Revision ID: 002
Revises: 001
Create Date: 2024-07-25 14:00:00.000000

Add patient profile information columns to users table.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add patient profile columns to users table."""
    # Patient Profile Information columns
    op.add_column("users", sa.Column("full_name", sa.String(255), nullable=True))
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("date_of_birth", sa.Date(), nullable=True))
    op.add_column("users", sa.Column("gender", sa.String(20), nullable=True))
    op.add_column("users", sa.Column("height_cm", sa.Float(), nullable=True))
    op.add_column("users", sa.Column("weight_kg", sa.Float(), nullable=True))

    # Medical History columns
    op.add_column("users", sa.Column("allergies", sa.Text(), nullable=True))
    op.add_column(
        "users", sa.Column("existing_conditions", sa.Text(), nullable=True)
    )
    op.add_column(
        "users", sa.Column("current_medications", sa.Text(), nullable=True)
    )
    op.add_column("users", sa.Column("medical_history", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove patient profile columns from users table."""
    # Remove Medical History columns
    op.drop_column("users", "medical_history")
    op.drop_column("users", "current_medications")
    op.drop_column("users", "existing_conditions")
    op.drop_column("users", "allergies")

    # Remove Patient Profile Information columns
    op.drop_column("users", "weight_kg")
    op.drop_column("users", "height_cm")
    op.drop_column("users", "gender")
    op.drop_column("users", "date_of_birth")
    op.drop_column("users", "age")
    op.drop_column("users", "full_name")
