from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.services.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.create_task(db, task_create)

@router.get("", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.get_tasks(db)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.update_task(db, task_id, task_update)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.get_task(db, task_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    task_service: TaskService = Depends(get_task_service),
):
    task_service.delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
