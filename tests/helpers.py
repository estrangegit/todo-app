from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.models.task import Task


def clear_database(session: Session) -> None:
    session.execute(delete(Task))
    session.commit()

def create_task(session: Session, title: str = "Task", status: TaskStatus = TaskStatus.TODO) -> Task:
    task = Task(title=title, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
