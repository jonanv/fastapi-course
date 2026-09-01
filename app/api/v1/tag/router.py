from typing import Any

from fastapi import APIRouter, Depends, Path, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.tag.repository import TagRepository
from app.api.v1.tag.schemas import TagCreate, TagPublic
from app.core.db import get_db
from app.core.security import get_current_user
from app.models.tag import TagORM

router = APIRouter(prefix="/tags", tags=["tag"])


@router.get("",  response_model=dict, response_description="Lista de post por paginación")
def list_tags(
    page: int = Query(
        1,
        ge=1,
        description="Número de página (mayor o igual a 1)"
    ),
    per_page: int = Query(
        10,
        ge=1,
        le=100,
        description="Número de resultados (1-50)"
    ),
    order_by: str = Query(
        "id",
        pattern="^(id|name|created_at)$",
        description="Campo de orden"
    ),
    direction: str = Query(
        "asc",
        pattern="^(asc|desc)$",
        description="Dirección de orden"
    ),
    search: str | None = Query(None),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    repository = TagRepository(db)
    return repository.list_tags(
        search=search,
        order_by=order_by,
        direction=direction,
        page=page,
        per_page=per_page
    )

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

@router.post("", response_model=TagPublic, response_description="Tag creada (OK)", status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> TagORM:
    repository =  TagRepository(db)
    
    try:
        new_tag = repository.create_tag(
            name=tag.name
        )
        db.commit()
        db.refresh(new_tag)
        return new_tag
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el tag")