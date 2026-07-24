from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_user_service
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(db, user_create)
