from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Task
from tests.helpers import clear_database

def test_get_tasks_returns_empty_list(client: TestClient, session: Session):
    clear_database(session)
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_should_create_and_return_task(client, session):
    clear_database(session)

    create_response = client.post(
        "/tasks",
        json={"title": "Apprendre FastAPI"}
    )
    assert create_response.status_code == 201

    created_task = create_response.json()

    assert created_task["title"] == "Apprendre FastAPI"
    assert created_task["status"] == "TODO"

    db_tasks = session.query(Task).all()

    assert len(db_tasks) == 1
    assert db_tasks[0].title == "Apprendre FastAPI"

    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    tasks = get_response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Apprendre FastAPI"
    assert tasks[0]["status"] == "TODO"
