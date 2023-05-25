"""create user table

Revision ID: f07d3f1f2fad
Revises: 
Create Date: 2023-05-25 19:35:43.514684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f07d3f1f2fad"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid, primary_key=True, index=True),
        sa.Column("full_name", sa.String, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_superuser", sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table("users")
