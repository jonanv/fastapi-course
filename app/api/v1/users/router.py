from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from .repository import UserRepository
from app.core.db import get_db
from app.core.security import require_admin
from app.models.user import UserORM

from .schemas import RoleUpdate, UserPublic

router = APIRouter(prefix="/users", tags=["user"])


@router.put("/role/{user_id}", response_model=UserPublic, response_description="Actualizar el rol de un usuario", status_code=status.HTTP_200_OK)
def set_role(
    user_id: int = Path(..., ge=1), 
    payload: RoleUpdate = None, 
    db: Session = Depends(get_db), 
    _admin: UserORM = Depends(require_admin)
) -> UserORM:
    repository = UserRepository(db)
    user = repository.get(user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    try:
        update_user = repository.set_role(user, payload.role)
        db.commit()
        db.refresh(update_user)
        return UserPublic.model_validate(update_user)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el rol")