from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title must not be blank")

        return value

class TaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: TaskStatus | None = None
