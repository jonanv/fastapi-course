from __future__ import annotations

from typing import Iterable, Sequence
from collections.abc import Iterable as IterableABC

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_many(self, *, skip: int = 0, limit: int = 50) -> Sequence[CategoryORM]:
        pass

    def list_with_total(self, *, page: int = 1, per_page: int = 50) -> tuple[int, list[CategoryORM]]:
        pass

    def get_category(self, category_id: int) -> CategoryORM | None:
        pass

    def get_by_slug(self, slug: str) -> CategoryORM | None:
        pass

    def create_category(self, *, name: str, slug: str) -> CategoryORM:
        pass

    def update_category(self, category: CategoryORM, updates: dict) -> CategoryORM:
        pass

    def delete_category(self, category: CategoryORM) -> None:
        pass