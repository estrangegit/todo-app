from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as task_router
from app.core.settings import settings
from app.api.exception_handlers import register_exception_handlers

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
)

app.include_router(health_router)
app.include_router(task_router)
register_exception_handlers(app)
