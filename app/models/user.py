from datetime import datetime
from typing import Literal

from sqlalchemy import Boolean, DateTime, Integer, String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

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