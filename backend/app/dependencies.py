from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.settings import Settings, get_settings
from app.services import jwt_service
from app.services.auth_service import AuthService
from app.services.password_service import PasswordService
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.services.jwt_service import JwtService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)

def get_task_service() -> TaskService:
    return TaskService()

def get_password_service() -> PasswordService:
    return PasswordService()

def get_jwt_service(settings: Settings = Depends(get_settings)) -> JwtService:
    return JwtService(settings)

def get_user_service(password_service: PasswordService = Depends(get_password_service)) -> UserService:
    return UserService(password_service)

def get_auth_service(password_service: PasswordService = Depends(get_password_service),
                     user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(password_service, user_service)
