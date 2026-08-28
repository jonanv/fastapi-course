from math import ceil

from fastapi import APIRouter, Query, Depends, Path, HTTPException, status
from typing import List, Optional, Literal, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.db import get_db
from app.models.post import PostORM
from .schemas import PaginatedPost, PostPublic, PostSummary, PostCreate, PostUpdate
from .repository import PostRespository
from app.core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["post"])


@router.get("",  response_model=PaginatedPost, response_description="Lista de post por paginación")
def list_posts(
    text: Optional[str] = Query(
        default=None, 
        deprecated=True,
        description="Parámetro obsoleto, usa 'query' o 'search' en su lugar."
    ),
    query: Optional[str] = Query(
        default=None, 
        description="Consulta de búsqueda para entradas de blog",
        alias="search",
        min_length=3,
        max_length=50,
        # pattern=r"^[\w\sáéíóúÁÉÍÓÚ-]+$"
        pattern=r"^[a-zA-Z]+$"
    ),
    per_page: int = Query(
        10,
        ge=1,
        le=50,
        description="Número de resultados (1-50)"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número de página (mayor o igual a 1)"
    ),
    # offset: int = Query(
    #     0,
    #     ge=0,
    #     description="Elementos a saltar antes de empezar la lista"
    # ),
    order_by: Literal["id", "title"] = Query(
        "id",
        description="Campo de orden"
    ),
    direction: Literal["asc", "desc"] = Query(
        "asc",
        description="Dirección de orden"
    ),
    db: Session = Depends(get_db)
) -> PaginatedPost:
    repository = PostRespository(db)
    query = query or text
    
    total, items = repository.search(
        query,
        order_by,
        direction,
        page,
        per_page
    )
    
    total_pages = ceil(total / per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(page, total_pages)
    
    has_prev = current_page > 1 if True else False
    has_next = current_page < total_pages if total_pages > 0 else False
    
    return PaginatedPost(
        page=current_page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        order_by=order_by,
        direction=direction,
        search=query,
        items=items
    )

@router.get("/by-tags", response_model=List[PostPublic], response_description="Filtrar post públicos por etiqueta")
def filter_by_tags(
    tags: List[str] = Query(
        ...,
        min_length=1,
        title="Filtro por etiqueta",
        description="Una o mas etiquetas. Ejemplo: ?tags=python&tags=fastapi",
        examples="?tags=python&tags=fastapi"
    ),
    db: Session = Depends(get_db)
) -> List[PostORM]:
    repository = PostRespository(db)
    posts = repository.by_tags(tags)
    return posts

@router.get("/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Buscar post por id")
def get_post(
    post_id: int = Path(
        ...,
        ge=1,
        title="Id del post",
        description="Identificador entero del post. debe ser mayor o igual a 1",
        examples=1    
    ), 
    include_content: bool | None = Query(
        default=True, 
        description="Incluir el contenido"
    ),
    db: Session = Depends(get_db)
) -> (PostPublic | PostSummary):
    repository = PostRespository(db)
    post = repository.get(post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    
    if include_content:
        return PostPublic.model_validate(post, from_attributes=True)
    
    return PostSummary.model_validate(post, from_attributes=True)

@router.post("", response_model=PostPublic, response_description="Post creado (OK)", status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> PostORM:
    repository = PostRespository(db)
    
    try:
        new_post = repository.create_post(
            title=post.title, 
            content=post.content, 
            author=user, 
            tags=[tag.model_dump() for tag in post.tags]
        )
        db.commit()
        db.refresh(new_post)
        return new_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre del título ya existe")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el post")

@router.put("/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True, status_code=status.HTTP_200_OK)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> PostORM:
    repository = PostRespository(db)
    post = repository.get(post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    
    try:
        updates = data.model_dump(exclude_unset=True)
        post = repository.update_post(post, updates)
        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar post")
        
@router.delete("/{post_id}", response_description="Post eliminado", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> dict[str, str]:
    repository = PostRespository(db)
    post = repository.get(post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    
    try:
        repository.delete_post(post)
        db.commit()
        return { "message": "Post eliminado" }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar post")