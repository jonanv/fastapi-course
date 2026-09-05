from contextlib import contextmanager
from typing import Optional
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM
from app.models.tag import TagORM
from app.models.user import UserORM


def hash_passwword(plain: str) -> str:
    return PasswordHash.recommended().hash(plain)

@contextmanager
def atomic(db: Session):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise
    
def _user_by_email(db: Session, email: str) -> Optional[UserORM]:
    query = (
        select(UserORM)
        .where(UserORM.email == email)
    )
    return db.execute(query).scalars().first()

def _category_by_slug(db: Session, slug: str) -> Optional[CategoryORM]:
    query = (
        select(CategoryORM)
        .where(CategoryORM.slug == slug)
    )
    return db.execute(query).scalars().first()

def _tag_by_name(db: Session, name: str) -> Optional[TagORM]:
    query = (
        select(TagORM)
        .where(TagORM.name == name)
    )
    return db.execute(query).scalars().first()