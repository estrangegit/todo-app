from pydantic import BaseModel, ConfigDict, field_validator, Field
from app.enums.user_role import UserRole

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)

    @field_validator("username", "password")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("must not be blank")

        return value

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)