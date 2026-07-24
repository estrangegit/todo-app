from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_jwt_service, get_user_service
from app.exceptions.invalid_token_exception import InvalidTokenException
from app.models.user import User
from app.services.jwt_service import JwtService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    jwt_service: JwtService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service)) -> User:

    payload = jwt_service.decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise InvalidTokenException()

    user = user_service.find_by_username(db, username)

    if user is None:
        raise InvalidTokenException()

    return user