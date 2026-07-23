from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.models import Task
from tests.helpers import clear_database, create_task

def test_get_tasks_returns_empty_list(client: TestClient, session: Session):
    clear_database(session)
    response = client.get("/tasks")
    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 0
    assert data["size"] == 20
    assert data["total_items"] == 0
    assert data["total_pages"] == 0
    assert len(data["items"]) == 0

def test_should_create_and_return_task(client: TestClient, session: Session):
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

    data = get_response.json()

    assert data["page"] == 0
    assert data["size"] == 20
    assert data["total_items"] == 1
    assert data["total_pages"] == 1
    assert len(data["items"]) == 1

    tasks = data["items"]

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Apprendre FastAPI"
    assert tasks[0]["status"] == "TODO"

def test_get_tasks_with_pagination(client: TestClient, session: Session):
    clear_database(session)

    for i in range(25):
        create_task(session, title=f"Task {i}")

    response = client.get("/tasks?page=0&size=10")

    data = response.json()

    assert data["page"] == 0
    assert data["size"] == 10
    assert data["total_items"] == 25
    assert data["total_pages"] == 3
    assert len(data["items"]) == 10

def test_get_tasks_filtered(client: TestClient, session: Session):
    clear_database(session)

    create_task(session, status=TaskStatus.TODO)
    create_task(session, status=TaskStatus.DONE)

    response = client.get("/tasks?status=TODO")

    data = response.json()

    assert data["total_items"] == 1
    assert data["items"][0]["status"] == "TODO"

def test_should_return_tasks_sorted_by_title_ascending(client: TestClient, session: Session):
    clear_database(session)

    # Given
    create_task(session, title="Charlie", status=TaskStatus.TODO)
    create_task(session, title="Alpha", status=TaskStatus.TODO)
    create_task(session, title="Bravo", status=TaskStatus.TODO)

    # When
    response = client.get("/tasks?sort=title&direction=asc")

    # Then
    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 3

    titles = [task["title"] for task in data["items"]]

    assert titles == [
        "Alpha",
        "Bravo",
        "Charlie",
    ]

def test_should_return_tasks_sorted_by_title_descending(client: TestClient, session: Session):
    clear_database(session)
    
    # Given
    create_task(session, title="Charlie", status=TaskStatus.TODO)
    create_task(session, title="Alpha", status=TaskStatus.TODO)
    create_task(session, title="Bravo", status=TaskStatus.TODO)

    # When
    response = client.get("/tasks?sort=title&direction=desc")

    # Then
    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data["items"]]

    assert titles == [
        "Charlie",
        "Bravo",
        "Alpha",
    ]
