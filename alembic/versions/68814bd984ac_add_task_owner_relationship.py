"""add task owner relationship

Revision ID: 68814bd984ac
Revises: fdfbf58f8d4f
Create Date: 2026-07-24 15:56:06.010762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68814bd984ac'
down_revision: Union[str, Sequence[str], None] = 'fdfbf58f8d4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM tasks")
    op.add_column('tasks', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("fk_tasks_owner_id_users", 'tasks', 'users', ['owner_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_tasks_owner_id_users", 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'owner_id')
