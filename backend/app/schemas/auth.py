from pydantic import BaseModel, field_validator, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)

    @field_validator("username", "password")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("must not be blank")

        return value

class LoginResponse(BaseModel):
    access_token: str
    token_type: str