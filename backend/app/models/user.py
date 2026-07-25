from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.user_role import UserRole

if TYPE_CHECKING:
    from app.models.task import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="userrole"), default=UserRole.USER, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", foreign_keys="Task.owner_id", cascade="all, delete-orphan")
