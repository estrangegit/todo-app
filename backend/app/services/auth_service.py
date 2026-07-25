from sqlalchemy.orm import Session

from app.exceptions.invalid_credentials_exception import InvalidCredentialsException
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.services.password_service import PasswordService
from app.services.user_service import UserService


class AuthService:

    def __init__(self, password_service: PasswordService, user_service: UserService):
        self._password_service = password_service
        self._user_service = user_service

    def authenticate(self, db: Session, login_request: LoginRequest) -> User:
        user = self._user_service.find_by_username(db, login_request.username)

        if user is None:
            raise InvalidCredentialsException()

        if not self._password_service.verify(login_request.password, user.password_hash):
            raise InvalidCredentialsException()

        return user
