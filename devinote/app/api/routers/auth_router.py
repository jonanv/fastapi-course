from typing import Any
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.api.dependencies import DBSession
from app.models.user import UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead, response_description="Registrar un nuevo usuario", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DBSession) -> UserCreate:
    service = AuthService(UserRepository(db))
    return service.register(payload)

@router.post("/login", response_model=Any, response_description="", status_code=status.HTTP_200_OK)
def login(email: str, password: str, db: DBSession) -> str:
    service = AuthService(UserRepository(db))
    token = service.login(email, password)
    return { "access_token": token, "token_type": "bearer" }

@router.post("/token", response_model=Any, response_description="", status_code=status.HTTP_200_OK)
def token(db: DBSession, form: OAuth2PasswordRequestForm = Depends()) -> str:
    email = form.username
    password = form.password
    service = AuthService(UserRepository(db))
    token = service.login(email, password)
    return { "access_token": token, "token_type": "bearer" }