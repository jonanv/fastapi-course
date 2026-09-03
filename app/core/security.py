from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

from ..models.user import UserORM
from ..core.config import Settings
from ..core.db import get_db
from ..services.exception import raise_no_authenticated, raise_expires_token, raise_forbidden, raise_invalid_credentials

password_hash = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=minutes or Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = { "sub": sub, "exp": expire }
    token = jwt.encode(payload=payload, key=Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
    return token

def decode_token(token: str) -> dict:
    payload = jwt.decode(jwt=token, key=Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])
    return payload

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)) -> UserORM:
    try:
        payload = decode_token(token)
        sub: Optional[str] = payload.get("sub")
        username: Optional[str] = payload.get("username")
        if not sub or not username:
            raise raise_no_authenticated()
        
        user_id = int(sub)
    except ExpiredSignatureError:
        raise raise_expires_token()
    except InvalidTokenError:
        raise raise_no_authenticated()
    except PyJWTError:
        raise raise_invalid_credentials()
    
    user = db.get(UserORM, user_id)
    
    if not user or not user.is_active:
        raise raise_invalid_credentials()
    
    return user
    
def hash_password(plain: str) -> str:
    return password_hash.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)