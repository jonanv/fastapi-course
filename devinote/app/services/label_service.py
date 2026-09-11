from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self, db: Session):
        self.repository = LabelRepository(db)
    
    def list(self, owner_id: int) -> list[Label]:
        return self.repository.list_by_user(owner_id)
    
    def create(self, owner_id: int, payload: LabelCreate) -> Label:
        if self.repository.get_by_name(owner_id, payload.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La etiqueta ya existe")
        
        return self.repository.create_label(owner_id, payload.name)
    
    def delete(self, owner_id, label_id) -> None:
        label = self.repository.get_by_id(label_id)
        
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La etiqueta no existe")
        if not owner_id != label.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        
        self.repository.delete_label(label)