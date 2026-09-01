from typing import Any, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.api.v1.tag.schemas import TagPublic
from app.models.post import PostORM, post_tags
from app.models.tag import TagORM
from app.services.pagination import paginate_query

class TagRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get(self, tag_id: int) -> Optional[TagORM]:
        tag_find = (
            select(TagORM)
            .where(TagORM.id == tag_id)
        )
        return self.db.execute(tag_find).scalar_one_or_none()
    
    def list_tags(
        self,
        search: Optional[str],
        order_by: str = "id",
        direction: str = "asc",
        page: int = 1,
        per_page: int = 10
    ) -> dict[str, Any]:
        query = select(TagORM)
        
        if search:
            query = query.where(func.lower(TagORM.name).ilike(f"%{ search.lower() }%"))
            
        allowed_order = {
            "id": TagORM.id,
            "name": func.lower(TagORM.name),
            "created_at": TagORM.created_at
        }
        
        result = paginate_query(
            db=self.db,
            modelORM=TagORM,
            base_query=query,
            page=page,
            per_page=per_page,
            order_by=order_by,
            direction=direction,
            allowed_order=allowed_order
        )
        # Valida o convierte un equivalente del ORM a un TagPublic para evitar el error de Pydentic, evita el error Pydentic serialization error
        result["items"] = [TagPublic.model_validate(item) for item in result["items"]]
        
        return result
    
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
    
    def update_tag(self, tag: TagORM, updates: dict) -> TagORM:
        for key, value in updates.items():
            setattr(tag, key, value)
        return tag
    
    def delete_tag(self, tag: TagORM) -> None:
        self.db.delete(tag)
        
    def most_popular(self) -> dict | None:
        
        row = (
            self.db.execute(
                select(
                    TagORM.id.label("id"),
                    TagORM.name.label("name"),
                    func.count(PostORM.id).label("uses")
                )
                .join(post_tags, post_tags.c.tag_id == TagORM.id)
                .join(PostORM, PostORM.id == post_tags.c.post_id)
                .group_by(TagORM.id, TagORM.name)
                .order_by(
                    func.count(PostORM.id).desc(),      # Primer citerio el id   
                    func.lower(TagORM.name).asc()       # Desempate del criterio por medio del nombre
                )
                .limit(1)
            )
            .mappings()   # mappings - Ayuda a convertir a diccionario
            .first()
        )
        
        return dict(row) if row else None 