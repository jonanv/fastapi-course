from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.user.repository import UserRepository
from app.core.db import get_db
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.models.user import UserORM
from app.services.exception import raise_invalid_credentials
from .schemas import TokenResponse
from ..user.schemas import UserCreate, UserLogin, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, response_description="Registrar usuario", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserORM:
    repository = UserRepository(db)
    user = repository.get_user_by_email(payload.email)
    
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    
    try:
        new_user = repository.create_user(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name
        )
        db.commit()
        db.refresh(new_user)
        return UserPublic.model_validate(new_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear usuario")
    
@router.post("/login", response_model=TokenResponse, response_description="Login de usuario")
async def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    repository = UserRepository(db)
    user = repository.get_user_by_email(payload.email)
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise raise_invalid_credentials()
    
    token = create_access_token(sub=str(user.id))
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))

@router.get("/me", response_model=UserPublic, response_description="")
async def read_me(current: UserORM = Depends(get_current_user)) -> dict[str, Any]:
    return UserPublic.model_validate(current)