from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.access_denied_exception import AccessDeniedException
from app.exceptions.invalid_credentials_exception import InvalidCredentialsException
from app.exceptions.invalid_token_exception import InvalidTokenException
from app.exceptions.task_not_found_exception import TaskNotFoundException
from app.exceptions.user_already_exists_exception import UserAlreadyExistsException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Task not found"},
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid username or password"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
        request: Request,
        exc: InvalidTokenException,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(AccessDeniedException)
    async def access_denied_exception_handler(
        request: Request,
        exc: InvalidTokenException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )
