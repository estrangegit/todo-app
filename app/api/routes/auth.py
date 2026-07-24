from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_auth_service, get_jwt_service
from app.schemas.auth import LoginResponse, LoginRequest
from app.services.auth_service import AuthService
from app.services.jwt_service import JwtService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
            db: Session = Depends(get_db),
            auth_service: AuthService = Depends(get_auth_service),
            jwt_service: JwtService = Depends(get_jwt_service)):
    login_request = LoginRequest(username=form_data.username, password=form_data.password)
    user = auth_service.authenticate(db, login_request)
    access_token = jwt_service.create_access_token(user)
    return LoginResponse(access_token=access_token, token_type="bearer")
