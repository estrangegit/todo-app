from fastapi import Depends

from app.services.password_service import PasswordService
from app.services.task_service import TaskService
from app.services.user_service import UserService


def get_task_service() -> TaskService:
    return TaskService()

def get_password_service() -> PasswordService:
    return PasswordService()

def get_user_service(password_service: PasswordService = Depends(get_password_service)) -> UserService:
    return UserService(password_service)
