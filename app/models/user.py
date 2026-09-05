from datetime import datetime
from typing import TYPE_CHECKING, Literal, List

from sqlalchemy import Boolean, DateTime, Integer, String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .post import PostORM

Role = Literal["user", "editor", "admin"]


class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="unique_user_email"),)
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum("user", "editor", "admin", name="rol_enum"), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    posts: Mapped[List["PostORM"]] = relationship(back_populates="user")