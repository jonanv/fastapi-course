from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

from ..api.v1.users.repository import UserRepository

from ..models.user import UserORM
from ..core.config import settings
from ..core.db import get_db
from ..services.exception import raise_no_authenticated, raise_expires_token, raise_forbidden, raise_invalid_credentials

password_hash = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def auth2_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict[str, str]:
    repository = UserRepository(db)
    user = repository.get_user_by_email(form.username)
    
    if not user or not verify_password(form.password, user.hashed_password):
        raise raise_invalid_credentials()
    
    token = create_access_token(sub=str(user.id))
    return { "access_token": token, "token_type": "bearer" }

def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = { "sub": sub, "exp": expire }
    token = jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_token(token: str) -> dict:
    payload = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)) -> UserORM:
    try:
        payload = decode_token(token)
        sub: Optional[str] = payload.get("sub")
        if not sub:
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

def require_role(min_role: Literal["user", "editor", "admin"]) -> UserORM:
    order = { "user": 0, "editor": 1, "admin": 2 }
    
    def evaluation(user = Depends(get_current_user)) -> UserORM:
        if order[user.role] < order[min_role]:
            raise raise_forbidden()
        return user
    
    return evaluation

require_user = require_role("user")
require_editor = require_role("editor")
require_admin = require_role("admin")