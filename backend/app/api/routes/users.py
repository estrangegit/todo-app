from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_user_service
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.security import require_roles, get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(db, user_create)

@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(current_user: User = Depends(require_roles(UserRole.ADMIN)),
              db: Session = Depends(get_db),
              user_service: UserService = Depends(get_user_service)):
    return user_service.get_users(db)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN))) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role
    )
