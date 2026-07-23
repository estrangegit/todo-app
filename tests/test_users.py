from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models import User
from tests.helpers import clear_database, create_user

def test_should_create_and_return_user(client: TestClient, session: Session):
    clear_database(session)

    create_response = client.post(
        "/users",
        json={"username": "user_1", "password": "password_user_1"},
    )
    assert create_response.status_code == 201

    created_user = create_response.json()

    assert created_user["username"] == "user_1"
    assert created_user["role"] == UserRole.USER.value

    db_users = session.query(User).all()

    assert len(db_users) == 1
    assert db_users[0].username == "user_1"
    assert db_users[0].role == UserRole.USER

def test_should_return_conflict_when_username_already_exists(client: TestClient, session: Session):
    # Given
    clear_database(session)

    create_user(session, username="user_1", password="password")

    # When
    response = client.post(
        "/users",
        json={"username": "user_1", "password": "another_password"},
    )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT

    users = session.query(User).all()

    assert len(users) == 1
    assert users[0].username == "user_1"
