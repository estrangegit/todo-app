from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.enums.user_role import UserRole
from app.models.task import Task
from app.models.user import User


def clear_database(session: Session) -> None:
    session.execute(delete(Task))
    session.execute(delete(User))
    session.commit()

def create_task(session: Session, title: str = "Task", status: TaskStatus = TaskStatus.TODO) -> Task:
    task = Task(title=title, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def create_user(session: Session, username: str = "User", password: str = "password", role: UserRole = UserRole.USER) -> User:
    user = User(username=username, password_hash=password, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
