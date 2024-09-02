"""Add_seed_data

Revision ID: c940bb925053
Revises: 5de8c455deab
Create Date: 2024-08-29 17:35:03.700168

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.utils import get_password_hash
from app.settings import USER_PASSWORD, ADMIN_PASSWORD


# revision identifiers, used by Alembic.
revision: str = "c940bb925053"
down_revision: Union[str, None] = "5de8c455deab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company = sa.table(
        "company",
        sa.column("id", sa.UUID),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
    )
    user = sa.table(
        "user",
        sa.column("id", sa.UUID),
        sa.column("email", sa.String),
        sa.column("username", sa.String),
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("hashed_password", sa.String),
        sa.column("is_active", sa.Boolean),
        sa.column("is_admin", sa.Boolean),
        sa.column("company_id", sa.UUID),
    )
    task = sa.table(
        "task",
        sa.column("id", sa.UUID),
        sa.column("summary", sa.String),
        sa.column("description", sa.String),
        sa.column("status", sa.Enum),
        sa.column("priority", sa.Integer),
        sa.column("user_id", sa.UUID),
    )

    # Insert data
    company_id = uuid.uuid4()
    op.bulk_insert(
        company,
        [
            {
                "id": company_id,
                "name": "Example Corp",
                "description": "An example company",
            }
        ],
    )

    # Insert user data
    admin_id = uuid.uuid4()
    user_id = uuid.uuid4()
    op.bulk_insert(
        user,
        [
            {
                "id": admin_id,
                "email": "admin@example.com",
                "username": "admin",
                "first_name": "Admin",
                "last_name": "Last_Name",
                "hashed_password": get_password_hash(ADMIN_PASSWORD),
                "is_active": True,
                "is_admin": True,
                "company_id": company_id,
            },
            {
                "id": user_id,
                "email": "user@example.com",
                "username": "user",
                "first_name": "User",
                "last_name": "Last_Name",
                "hashed_password": get_password_hash(USER_PASSWORD),
                "is_active": True,
                "is_admin": False,
                "company_id": company_id,
            },
        ],
    )

    # Insert task data
    op.bulk_insert(
        task,
        [
            {
                "id": uuid.uuid4(),
                "summary": "Admin task",
                "description": "This is the first task",
                "status": "NEW",
                "priority": 1,
                "user_id": admin_id,
            },
            {
                "id": uuid.uuid4(),
                "summary": "User task",
                "description": "This is the first task",
                "status": "NEW",
                "priority": 1,
                "user_id": user_id,
            },
        ],
    )


def downgrade() -> None:
    # Define table constructs again for the downgrade function
    company = sa.table("company")
    user = sa.table("user")
    task = sa.table("task")

    # Remove inserted data
    op.execute(task.delete())
    op.execute(user.delete())
    op.execute(company.delete())
