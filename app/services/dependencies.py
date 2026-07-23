from app.services.task_service import TaskService
from app.services.user_service import UserService


def get_task_service() -> TaskService:
    return TaskService()

def get_user_service() -> UserService:
    return UserService()