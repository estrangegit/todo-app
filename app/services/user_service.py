from sqlalchemy.orm import Session

from app.exceptions.user_already_exists_exception import UserAlreadyExistsException
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        self._check_username_available(db, user_create.username)

        user = User (
            username=user_create.username,
            password_hash=user_create.password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def _check_username_available(self, db: Session, username: str) -> None:
        existing_user = (db.query(User).filter(User.username == username).first())
        if existing_user is not None:
            raise UserAlreadyExistsException(username)