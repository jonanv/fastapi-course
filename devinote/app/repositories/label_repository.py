from sqlmodel import Session, select, delete

from devinote.app.models.label import Label, NoteLabelLink
from devinote.app.models.share import LabelShare


class LabelRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def list_by_user(self, owner_id: int) -> list[Label]:
        query = (
            select(Label)
            .where(Label.owner_id == owner_id)
            .order_by(Label.name.desc())
        )
        return self.db.exec(query).all()
    
    def get_by_id(self, label_id: int) -> Label | None:
        return self.db.get(Label, label_id)
    
    def get_by_name(self, owner_id: int, name: str) -> Label | None:
        query = (
            select(Label)
            .where(Label.owner_id == owner_id, Label.name == name)
        )
        return self.db.exec(query).first()
    
    def create_label(self, owner_id: int, name: str) -> Label:
        label = Label(name=name, owner_id=owner_id)
        self.db.add(label)
        self.db.flush()
        self.db.commit()
        self.db.refresh(label)
        return label
    
    def delete_label(self, label: Label) -> None:
        query = (
            delete(NoteLabelLink)
            .where(NoteLabelLink.label_id == label.id)
        )
        self.db.exec(query)
        
        query = (
            delete(LabelShare)
            .where(LabelShare.label_id == label.id)
        )
        self.db.exec(query)
        self.db.delete(label)
        self.db.commit()