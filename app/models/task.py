from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.enums.task_status import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus, name="taskstatus"), default=TaskStatus.TODO, nullable=False)
