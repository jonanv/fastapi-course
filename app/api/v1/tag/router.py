from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.api.v1.tag.repository import TagRepository
from app.api.v1.tag.schemas import TagCreate, TagPublic
from app.core.db import get_db
from app.models.tag import TagORM

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

@router.post("", response_model=TagCreate, response_description="Tag creada (OK)", status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
) -> TagORM:
    repository =  TagRepository(db)
    
    try:
        new_tag = repository.create_tag(
            name=tag.name
        )
        db.commit()
        db.refresh(new_tag)
        return new_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de la etiqueta ya existe")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el tag")