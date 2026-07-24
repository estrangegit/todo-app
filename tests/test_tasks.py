from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.models import Task
from app.models.user import User
from tests.helpers import clear_database, create_task, create_user, auth_headers


def test_get_tasks_returns_empty_list(client: TestClient, session: Session):
    clear_database(session)

    create_user(session)
    response = client.get("/tasks", headers=auth_headers(client))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["page"] == 0
    assert data["size"] == 20
    assert data["total_items"] == 0
    assert data["total_pages"] == 0
    assert len(data["items"]) == 0

def test_create_task_requires_authentication(client: TestClient):
    response = client.post(
        "/tasks",
        json={
            "title": "Buy milk",
            "status": "TODO",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_authenticated_user_can_create_task(client: TestClient, session: Session):
    clear_database(session)

    create_user(session)
    create_response = client.post(
        "/tasks",
        json={"title": "Apprendre FastAPI"},
        headers=auth_headers(client)
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    created_task = create_response.json()

    assert created_task["title"] == "Apprendre FastAPI"
    assert created_task["status"] == "TODO"

    db_tasks = session.query(Task).all()

    assert len(db_tasks) == 1
    assert db_tasks[0].title == "Apprendre FastAPI"

    get_response = client.get("/tasks", headers=auth_headers(client))
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


def test_created_task_is_owned_by_authenticated_user(client: TestClient, session: Session):
    clear_database(session)
    user: User = create_user(session)
    response = client.post("/tasks", json={"title": "Buy milk", "status": "TODO"}, headers=auth_headers(client))
    assert response.status_code == status.HTTP_201_CREATED
    task = session.query(Task).one()
    assert task.owner_id == user.id

def test_get_tasks_with_pagination(client: TestClient, session: Session):
    clear_database(session)
    user: User = create_user(session)

    for i in range(25):
        create_task(session, user, title=f"Task {i}")


    response = client.get("/tasks?page=0&size=10", headers=auth_headers(client))

    data = response.json()

    assert data["page"] == 0
    assert data["size"] == 10
    assert data["total_items"] == 25
    assert data["total_pages"] == 3
    assert len(data["items"]) == 10

def test_get_tasks_filtered(client: TestClient, session: Session):
    clear_database(session)
    user: User = create_user(session)

    create_task(session, user, status=TaskStatus.TODO)
    create_task(session, user, status=TaskStatus.DONE)

    response = client.get("/tasks?status=TODO", headers=auth_headers(client))

    data = response.json()

    assert data["total_items"] == 1
    assert data["items"][0]["status"] == "TODO"

def test_should_return_tasks_sorted_by_title_ascending(client: TestClient, session: Session):
    clear_database(session)
    user: User = create_user(session)

    # Given
    create_task(session, user, title="Charlie", status=TaskStatus.TODO)
    create_task(session, user, title="Alpha", status=TaskStatus.TODO)
    create_task(session, user, title="Bravo", status=TaskStatus.TODO)

    # When
    response = client.get("/tasks?sort=title&direction=asc", headers=auth_headers(client))

    # Then
    assert response.status_code == status.HTTP_200_OK

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
    user: User = create_user(session)
    
    # Given
    create_task(session, user, title="Charlie", status=TaskStatus.TODO)
    create_task(session, user, title="Alpha", status=TaskStatus.TODO)
    create_task(session, user, title="Bravo", status=TaskStatus.TODO)

    # When
    response = client.get("/tasks?sort=title&direction=desc", headers=auth_headers(client))

    # Then
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    titles = [task["title"] for task in data["items"]]

    assert titles == [
        "Charlie",
        "Bravo",
        "Alpha",
    ]
