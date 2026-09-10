from __future__ import annotations

from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .post import PostORM


class CategoryORM(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("name", name="unique_category_name"),)
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)
    
    posts: Mapped[List["PostORM"]] = relationship(
        back_populates="category", # Establece la relación inversa con la clase PostORM
        cascade="all, delete", 
        passive_deletes=True
    )