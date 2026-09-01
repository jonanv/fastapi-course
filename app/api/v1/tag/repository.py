from sqlalchemy import select, func
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
        normalize = name.strip().lower()
                
        tag_obj = self.db.execute(
            select(TagORM)
            .where(func.lower(TagORM.name) ==  normalize) # Para Postgre -> TagORM.name.ilike(normalize)
        ).scalar_one_or_none()
        
        if tag_obj:
            return tag_obj
            
        tag_obj = TagORM(name=name)
        self.db.add(tag_obj)
        self.db.flush()
        
        return tag_obj