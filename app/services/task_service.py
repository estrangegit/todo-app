from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.exceptions.task import TaskNotFoundException
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def create_task(self, db: Session, task_create: TaskCreate) -> Task:
        task = Task(
            title=task_create.title,
            status=TaskStatus.TODO
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    def get_tasks(self, db: Session) -> list[Task]:
        return db.query(Task).all()

    def update_task(self, db: Session, task_id: int, task_update: TaskUpdate) -> Task:
        task = self._get_task_or_404(db, task_id)

        update_data = task_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task

    def get_task(self, db: Session, task_id: int) -> Task:
        task = self._get_task_or_404(db, task_id)
        return task

    def delete_task(self, db: Session, task_id: int) -> None:
        task = self._get_task_or_404(db, task_id)
        db.delete(task)
        db.commit()

    def _get_task_or_404(self, db: Session, task_id: int) -> Task:
        task = db.get(Task, task_id)

        if task is None:
            raise TaskNotFoundException()

        return task