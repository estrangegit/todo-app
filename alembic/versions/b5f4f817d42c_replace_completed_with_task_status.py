"""replace completed with task status

Revision ID: b5f4f817d42c
Revises: 086e50105694
Create Date: 2026-07-22 17:52:15.650565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5f4f817d42c'
down_revision: Union[str, Sequence[str], None] = '086e50105694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    task_status = sa.Enum(
        "TODO",
        "IN_PROGRESS",
        "DONE",
        name="taskstatus",
    )

    task_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "tasks",
        sa.Column(
            "status",
            task_status,
            nullable=True,
        ),
    )

    op.execute("""
        UPDATE tasks
        SET status =
        CASE
            WHEN completed THEN 'DONE'::taskstatus
            ELSE 'TODO'::taskstatus
        END
    """)

    op.alter_column(
        "tasks",
        "status",
        nullable=False,
    )

    op.drop_column("tasks", "completed")


def downgrade() -> None:
    """Downgrade schema."""

    task_status = sa.Enum(
        "TODO",
        "IN_PROGRESS",
        "DONE",
        name="taskstatus",
    )

    op.add_column(
        "tasks",
        sa.Column(
            "completed",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.execute("""
        UPDATE tasks
        SET completed =
        CASE
            WHEN status = 'DONE'::taskstatus THEN TRUE
            ELSE FALSE
        END
    """)

    op.alter_column(
        "tasks",
        "completed",
        nullable=False,
    )

    op.drop_column("tasks", "status")

    task_status.drop(op.get_bind(), checkfirst=True)
