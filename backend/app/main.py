from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as task_router
from app.api.routes.users import router as user_router
from app.core.settings import settings

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
)

app.include_router(health_router, prefix='/api')
app.include_router(task_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(auth_router, prefix='/api')
register_exception_handlers(app)
