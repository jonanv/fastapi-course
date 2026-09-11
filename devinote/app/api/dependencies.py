from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.repositories.user_repository import UserRepository
from app.core.security import decode_token
from app.models.user import User
from app.db.database import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_db() -> Session:
    return next(get_session())

# db: Session = Depedens(get_db)
DBSession = Annotated[Session, Depends(get_db)]
# db: DBSession

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DBSession) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="No autorizado",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise credentials_exception
    
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    
    if not user:
        raise credentials_exception
    
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]