from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import TagORM

class TagRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get(self, tag_id: int):
        tag_find = (
            select(TagORM)
            .where(TagORM.id == tag_id)
        )
        return self.db.execute(tag_find).scalar_one_or_none()
    
    def create_tag(self, name: str) -> TagORM:
        new_tag = TagORM(name=name)
        
        self.db.add(new_tag)
        self.db.flush()
        self.db.refresh(new_tag)
        return new_tag