from sqlalchemy import delete
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.enums.task_status import TaskStatus
from app.enums.user_role import UserRole
from app.models.task import Task
from app.models.user import User
from app.services.password_service import PasswordService

password_service = PasswordService()

def clear_database(session: Session) -> None:
    session.execute(delete(Task))
    session.execute(delete(User))
    session.commit()

# ========= Users =========

def create_user(session: Session, username: str = "john", password: str = "secret",role: UserRole = UserRole.USER) -> User:
    user = User(
        username=username,
        password_hash=password_service.hash(password),
        role=role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def get_access_token(client: TestClient, username: str = "john", password: str = "secret") -> str:
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, (
        f"Login failed: {response.status_code} - {response.text}"
    )
    return response.json()["access_token"]

def auth_headers(client: TestClient, username: str = "john", password: str = "secret") -> dict[str, str]:
    token = get_access_token(client, username, password)
    return {"Authorization": f"Bearer {token}"}


# ========= Tasks =========

def create_task(session: Session, title: str = "Task", status: TaskStatus = TaskStatus.TODO) -> Task:
    task = Task(title=title, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
