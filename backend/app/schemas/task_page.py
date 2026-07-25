from pydantic import BaseModel
from app.schemas.task import TaskResponse

class TaskPage(BaseModel):
    items: list[TaskResponse]
    page: int
    size: int
    total_items: int
    total_pages: int
