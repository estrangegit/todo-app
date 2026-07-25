from datetime import timezone, timedelta, datetime

import jwt
from jwt import InvalidTokenError

from app.core.settings import Settings
from app.exceptions.invalid_token_exception import InvalidTokenException
from app.models.user import User

class JwtService:

    def __init__(self, settings: Settings):
        self._settings = settings

    def create_access_token(self, user: User) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=self._settings.jwt_access_token_expire_minutes
        )

        payload = {"sub": user.username, "exp": expires_at}
        return jwt.encode(payload, self._settings.jwt_secret_key, algorithm=self._settings.jwt_algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._settings.jwt_secret_key, algorithms=[self._settings.jwt_algorithm])
        except InvalidTokenError as e:
            raise InvalidTokenException() from e
