from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Sequence
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.category import CategoryORM

from .repository import CategoryRepository
from app.core.db import get_db
from .schemas import CategoryCreate, CategoryUpdate, CategoryPublic

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("", response_model=list[CategoryPublic])
def list_categories(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)) -> Sequence[CategoryORM]:
    repository = CategoryRepository(db)
    return repository.list_many(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryPublic)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryPublic:
    repository = CategoryRepository(db)
    category = repository.get_category(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    return CategoryPublic.model_validate(category, from_attributes=True)

@router.post("", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)) -> CategoryORM:
    repository = CategoryRepository(db)
    exist = repository.get_category_by_slug(category.slug)
    
    if exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug en uso")
    
    try:
        new_category = repository.create_category(
            name=category.name,
            slug=category.slug
        )
        db.commit()
        db.refresh(new_category)
        return new_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de la categoría ya existe")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear categoría")

@router.put("/{category_id}", response_model=CategoryPublic, status_code=status.HTTP_200_OK)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)) -> CategoryORM:
    repository = CategoryRepository(db)
    category = repository.get_category(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    try:
        updates = data.model_dump(exclude_unset=True)
        category = repository.update_category(category, updates)
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar categoría")

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    repository = CategoryRepository(db)
    category = repository.get_category(category_id)
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    try:
        repository.delete_category(category)
        db.commit()
        return { "message": "Categoría eliminada" }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar categoría")