from math import ceil

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_task_service
from app.enums.sort_direction import SortDirection
from app.enums.task_sort_field import TaskSortField
from app.enums.task_status import TaskStatus
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.task_page import TaskPage
from app.security import require_roles
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER))
):
    return task_service.create_task(db, task_create)

@router.get("", response_model=TaskPage)
def get_tasks(
    status: TaskStatus | None = Query(default=None),
    page: int = Query(default=0, ge=0),
    size: int = Query(default=20, ge=1, le=100),
    sort: TaskSortField = Query(default=TaskSortField.ID),
    direction: SortDirection = Query(default=SortDirection.ASC),
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER))
):
    page = task_service.get_tasks(db, status, sort, direction, page, size)

    return TaskPage(
        items=page.items,
        page=page.page,
        size=page.size,
        total_items=page.total_items,
        total_pages=ceil(page.total_items / page.size),
    )

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER))
):
    return task_service.update_task(db, task_id, task_update)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER))
):
    return task_service.get_task(db, task_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER))
):
    task_service.delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
