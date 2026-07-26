from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.password_service import PasswordService
from app.services.user_service import UserService


def create_users(db: Session) -> dict[str, User]:
    user_service = UserService(PasswordService())

    admin = user_service.create_user(
        db,
        UserCreate(
            username="admin",
            password="123456",
        ),
        UserRole.ADMIN,
    )

    alice = user_service.create_user(
        db,
        UserCreate(
            username="alice",
            password="123456",
        ),
    )

    bob = user_service.create_user(
        db,
        UserCreate(
            username="bob",
            password="123456",
        ),
    )

    return {
        "admin": admin,
        "alice": alice,
        "bob": bob,
    }
