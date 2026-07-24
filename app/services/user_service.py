from sqlalchemy import select
from sqlalchemy.orm import Session
from app.exceptions.user_already_exists_exception import UserAlreadyExistsException
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.password_service import PasswordService

class UserService:

    def __init__(self, password_service: PasswordService):
        self._password_service = password_service

    def find_by_username(self, db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return db.scalar(stmt)

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        self._check_username_available(db, user_create.username)

        password_hash = self._password_service.hash(user_create.password)

        user = User (
            username=user_create.username,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def _check_username_available(self, db: Session, username: str) -> None:
        existing_user = (db.query(User).filter(User.username == username).first())
        if existing_user is not None:
            raise UserAlreadyExistsException(username)
