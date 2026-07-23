from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.task import TaskNotFoundException
from app.exceptions.user_already_exists_exception import UserAlreadyExistsException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": "Task not found"},
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )