"""create_user_task_company_tables

Revision ID: 5de8c455deab
Revises: 
Create Date: 2024-08-29 17:33:37.474697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM


# revision identifiers, used by Alembic.
revision: str = '5de8c455deab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM type if it doesn't exist
    status_enum = ENUM('NEW', 'IN_PROGRESS', 'PENDING', 'ABANDONED', 'DONE', name='status', create_type=False)
    status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "company",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column("company_id", UUID(as_uuid=True), nullable=False),
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "task",
        sa.Column("summary", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("status", status_enum, nullable=False, server_default="NEW"),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("assigner_id", UUID(as_uuid=True), nullable=False),
        sa.Column("doer_id", UUID(as_uuid=True), nullable=False),
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["assigner_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["doer_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    op.drop_table('task')
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table('user')
    op.drop_table('company')
    
    # Drop the ENUM type
    status_enum = ENUM('NEW', 'IN_PROGRESS', 'PENDING', 'ABANDONED', 'DONE', name='status')
    status_enum.drop(op.get_bind(), checkfirst=True)
    
    
    
