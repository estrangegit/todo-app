from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models import User
from app.services.password_service import PasswordService
from tests.helpers import clear_database, create_user, auth_headers


def test_should_create_and_return_user(client: TestClient, session: Session, password_service: PasswordService):
    clear_database(session)

    create_response = client.post(
        "/api/users",
        json={"username": "user_1", "password": "password_user_1"}
    )
    assert create_response.status_code == 201

    created_user = create_response.json()

    assert created_user["username"] == "user_1"
    assert created_user["role"] == UserRole.USER.value

    db_users = session.query(User).all()

    assert len(db_users) == 1
    assert db_users[0].username == "user_1"
    assert db_users[0].role == UserRole.USER

    assert db_users[0].password_hash != "password_user_1"

    assert password_service.verify(
        "password_user_1",
        db_users[0].password_hash,
    )


def test_should_return_conflict_when_username_already_exists(client: TestClient, session: Session):
    # Given
    clear_database(session)
    create_user(session, username="user_1", password="password")

    # When
    response = client.post(
        "/api/users",
        json={"username": "user_1", "password": "another_password"}
    )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT

    users = session.query(User).all()

    assert len(users) == 1
    assert users[0].username == "user_1"

def test_get_users_requires_authentication(client: TestClient):
    response = client.get("/api/users")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_admin_can_get_all_users(client: TestClient, session: Session):
    clear_database(session)

    create_user(session, "username_1", "password_1")
    create_user(session, "username_2", "password_2")

    create_user(session, username="john", password="secret", role=UserRole.ADMIN)
    response = client.get("/api/users", headers=auth_headers(client, "john", "secret"))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    usernames = [user["username"] for user in data]
    assert usernames == ["username_1", "username_2", "john"]

def test_non_admin_cannot_get_all_users(client: TestClient, session: Session):
    clear_database(session)

    create_user(session, "username_1", "password_1")
    create_user(session, "username_2", "password_2")

    create_user(session, username="john", password="secret", role=UserRole.USER)
    response = client.get("/api/users", headers=auth_headers(client))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert "detail" in data
