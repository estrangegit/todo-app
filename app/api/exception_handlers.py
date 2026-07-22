from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.task import TaskNotFoundException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": "Task not found"},
        )
