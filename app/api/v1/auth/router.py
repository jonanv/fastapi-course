from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, get_current_user, oauth2_schema
from .schemas import TokenResponse, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])

FAKE_USERS = {
    "ricardo@example.com": {"email": "ricardo@example.com", "username": "ricardo", "password": "secret123"},
    "alumno@example.com":  {"email": "alumno@example.com",  "username": "alumno",  "password": "123456"},
}

@router.get("/secure")
def secure_endpoit(token: str = Depends(oauth2_schema)) -> dict[str, str]:
    return { "message": "Acceso con token", "token_recibido": token }

@router.post("/login", response_model=Token, response_description="Login de usuario")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = FAKE_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
        
    token = create_access_token(
        data={ "sub": user["email"], "username": user["username"] },
        expires_delta=timedelta(minutes=30)
    )
    
    return { "access_token": token, "token_type": "bearer" }

@router.get("/me", response_model=UserPublic, response_description="")
async def read_me(current=Depends(get_current_user)) -> dict[str, Any]:
    return { "email": current["email"], "username": current["username"] }