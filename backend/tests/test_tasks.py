from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.models import Task
from app.models.user import User
from tests.helpers import clear_database, create_task, create_user, auth_headers, get_access_token


def test_create_task_requires_authentication(client: TestClient):
    response = client.post(
        "/api/tasks",
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
        "/api/tasks",
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

    get_response = client.get("/api/tasks", headers=auth_headers(client))
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
    response = client.post("/api/tasks", json={"title": "Buy milk", "status": "TODO"}, headers=auth_headers(client))
    assert response.status_code == status.HTTP_201_CREATED
    task = session.query(Task).one()
    assert task.owner_id == user.id

def test_get_tasks_returns_empty_list(client: TestClient, session: Session):
    clear_database(session)

    create_user(session)
    response = client.get("/api/tasks", headers=auth_headers(client))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["page"] == 0
    assert data["size"] == 20
    assert data["total_items"] == 0
    assert data["total_pages"] == 0
    assert len(data["items"]) == 0

def test_get_tasks_with_pagination(client: TestClient, session: Session):
    clear_database(session)
    user: User = create_user(session)

    for i in range(25):
        create_task(session, user, title=f"Task {i}")


    response = client.get("/api/tasks?page=0&size=10", headers=auth_headers(client))

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

    response = client.get("/api/tasks?status=TODO", headers=auth_headers(client))

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
    response = client.get("/api/tasks?sort=title&direction=asc", headers=auth_headers(client))

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
    response = client.get("/api/tasks?sort=title&direction=desc", headers=auth_headers(client))

    # Then
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    titles = [task["title"] for task in data["items"]]

    assert titles == [
        "Charlie",
        "Bravo",
        "Alpha",
    ]

def test_user_can_only_see_own_tasks(client: TestClient, session: Session):
    clear_database(session)
    alice = create_user(session, username="alice")
    bob = create_user(session, username="bob")

    create_task(session, title="Alice task 1", owner=alice)
    create_task(session, title="Alice task 2", owner=alice)
    create_task(session, title="Bob task", owner=bob)

    response = client.get(
        "/api/tasks",
        headers=auth_headers(client, "alice", "secret"),
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data["items"]) == 2
    assert {task["title"] for task in data["items"]} == {
        "Alice task 1",
        "Alice task 2",
    }

def test_user_with_no_tasks_gets_empty_list(client: TestClient, session: Session):
    clear_database(session)
    alice = create_user(session, username="alice")
    bob = create_user(session, username="bob")

    create_task(session, title="Alice task 1", owner=alice)
    create_task(session, title="Alice task 2", owner=alice)

    response = client.get(
        "/api/tasks",
        headers=auth_headers(client, "bob", "secret"),
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data["items"]) == 0

def test_user_can_get_own_task(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.get(f"/api/tasks/{task.id}", headers=auth_headers(client))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == task.id
    assert data["title"] == task.title
    assert data["status"] == task.status.value

def test_user_cannot_get_another_users_task(client: TestClient, session: Session):
    clear_database(session)
    alice = create_user(session, username="alice")
    bob = create_user(session, username="bob")

    task = create_task(session, owner=alice)

    response = client.get(f"/api/tasks/{task.id}", headers=auth_headers(client, username="bob"))

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_task_requires_authentication(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.get(f"/api/tasks/{task.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_user_can_update_own_task(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.patch(f"/api/tasks/{task.id}",
        json={
            "title": "Updated title",
            "status": "IN_PROGRESS",
        },
        headers=auth_headers(client),
    )

    assert response.status_code == status.HTTP_200_OK
    session.refresh(task)

    assert task.title == "Updated title"
    assert task.status == TaskStatus.IN_PROGRESS

def test_user_cannot_update_another_users_task(client: TestClient, session: Session):
    clear_database(session)
    alice = create_user(session, username="alice")
    bob = create_user(session, username="bob")

    task = create_task(session, owner=alice)

    # Act
    response = client.patch(
        f"/api/tasks/{task.id}",
        json={
            "title": "Hacked",
            "status": "DONE",
        },
        headers=auth_headers(client, username=bob.username),
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

    unchanged_task = session.get(Task, task.id)

    assert unchanged_task.title == task.title
    assert unchanged_task.status == task.status

def test_update_task_requires_authentication(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.patch(
        f"/api/tasks/{task.id}",
        json={
            "title": "Updated title",
            "status": "DONE",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_user_can_delete_own_task(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers(client))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db_tasks = session.query(Task).all()
    assert len(db_tasks) == 0

def test_user_cannot_delete_another_users_task(client: TestClient, session: Session):
    clear_database(session)
    alice = create_user(session, username="alice")
    bob = create_user(session, username="bob")

    task = create_task(session, owner=alice)

    response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers(client, username=bob.username))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert session.get(Task, task.id) is not None

def test_delete_task_requires_authentication(client: TestClient, session: Session):
    clear_database(session)
    user = create_user(session)
    task = create_task(session, owner=user)

    response = client.delete(f"/api/tasks/{task.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
