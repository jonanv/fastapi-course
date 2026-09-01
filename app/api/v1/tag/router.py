from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.tag.repository import TagRepository
from app.api.v1.tag.schemas import TagPublic
from app.core.db import get_db

router = APIRouter(prefix="/tags", tags=["tag"])

@router.get("/{tag_id}", response_model=TagPublic, response_description="Obtener etiqueta por id")
def get_tag(
    tag_id: int = Path(
        ...,
        ge=1,
        title="Id del tag",
        description="Identificador entero del tag. debe ser mayor o igual a 1",
        examples=1
    ), 
    db: Session = Depends(get_db)
) -> TagPublic:
    repository = TagRepository(db)
    tag = repository.get(tag_id)
    
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag no encontrado")
    
    return TagPublic.model_validate(tag, from_attributes=True)