from math import ceil

from sqlalchemy.orm import Session, Query

from app.enums.sort_direction import SortDirection
from app.enums.task_sort_field import TaskSortField
from app.enums.task_status import TaskStatus
from app.exceptions.task_not_found_exception import TaskNotFoundException
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.domain.page import Page


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

    def get_tasks(self,
                  db: Session,
                  status: TaskStatus | None = None,
                  sort: TaskSortField = TaskSortField.ID,
                  direction: SortDirection = SortDirection.ASC,
                  page: int = 0,
                  size: int = 20) -> Page[Task]:

        query = db.query(Task)

        if status is not None:
            query = query.filter(Task.status == status)

        query = self._apply_sort(query, sort, direction)

        total_items = query.count()

        query = query.offset(page * size)
        query = query.limit(size)

        items = (query.offset(page * size).limit(size).all())

        return Page(items=items, page=page, size=size, total_items=total_items)

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

    def _apply_sort(self, query: Query, sort: TaskSortField, direction: SortDirection) -> Query:

        sort_columns = {
            TaskSortField.ID: Task.id,
            TaskSortField.TITLE: Task.title,
            TaskSortField.STATUS: Task.status,
        }

        sort_column = sort_columns[sort]

        if direction == SortDirection.ASC:
            return query.order_by(sort_column.asc())

        return query.order_by(sort_column.desc())
