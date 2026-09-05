from __future__ import annotations

from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_many(self, *, skip: int = 0, limit: int = 50) -> Sequence[CategoryORM]:
        query = (
            select(CategoryORM)
            .offset(skip)
            .limit(limit)
        )
        return self.db.execute(query).scalars().all()

    def list_with_total(self, *, page: int = 1, per_page: int = 50) -> tuple[int, list[CategoryORM]]:
        total = self.db.scalar(
            select(func.count())
            .select_from(CategoryORM)
        ) or 0
        
        if total == 0:
            return 0, []
        
        total_pages = (total + per_page - 1) // per_page
        current_page = min(page, max(1, total_pages))
        offset = (current_page - 1) * per_page
        
        query = (
            select(CategoryORM)
            .offset(offset)
            .limit(per_page)
        )
        items = self.db.execute(query).scalars().all()
        return total, items

    def get_category(self, category_id: int) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def get_category_by_slug(self, slug: str) -> CategoryORM | None:
        query = (
            select(CategoryORM)
            .where(CategoryORM.slug == slug)
        )
        return self.db.execute(query).scalars().first()

    def create_category(self, *, name: str, slug: str) -> CategoryORM:
        new_category = CategoryORM(name=name, slug=slug)
        
        self.db.add(new_category)
        self.db.flush()
        self.db.refresh(new_category)
        return new_category

    def update_category(self, category: CategoryORM, updates: dict) -> CategoryORM:
        for key, value in updates.items():
            setattr(category, key, value)
        
        self.db.add(category)
        self.db.flush()
        self.db.refresh(category)
        return category

    def delete_category(self, category: CategoryORM) -> None:
        return self.db.delete(category)
        