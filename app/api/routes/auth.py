from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.auth import User
from app.schemas.auth import UserCreate, UserOut, Token, TokenRequest, TokenResponse
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)

@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   return auth_service.authenticate_user(db, form_data.username, form_data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(request: TokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, request.refresh_token)

@router.post("/auth/logout")
def logout_user(request: TokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return auth_service.logout(db, request.refresh_token)