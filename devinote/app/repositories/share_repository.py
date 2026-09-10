from sqlmodel import Session, select, delete

from devinote.app.models.share import NoteShare, LabelShare


class ShareRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def upsert_note_share(self, note_id: int, user_id: int, role: str) -> NoteShare:
        note_share = self.db.exec(
            select(NoteShare)
            .where(NoteShare.note_id == note_id, NoteShare.user_id == user_id)
        ).first()
        
        if note_share:
            note_share.role = role
            self.db.add(note_share)
            self.db.flush()
            self.db.commit()
            self.db.refresh(note_share)
            return note_share
        
        note_share = NoteShare(note_id=note_id, user_id=user_id, role=role)
        self.db.add(note_share)
        self.db.flush()
        self.db.commit()
        self.db.refresh(note_share)
        return note_share
    
    def remove_note_share(self, note_id: int, user_id: int) -> None:
        self.db.exec(
            delete(NoteShare)
            .where(NoteShare.note_id == note_id, NoteShare.user_id == user_id)
        )
        self.db.commit()
    
    def upsert_label_share(self, label_id: int, user_id: int, role: str) -> LabelShare:
        label_share = self.db.exec(
            select(LabelShare)
            .where(LabelShare.label_id == label_id, LabelShare.user_id == user_id)
        ).first()
        
        if label_share:
            label_share.role = role
            self.db.add(label_share)
            self.db.flush()
            self.db.commit()
            self.db.refresh(label_share)
            return label_share
        
        label_share = LabelShare(label_id=label_id, user_id=user_id, role=role)
        self.db.add(label_share)
        self.db.flush()
        self.db.commit()
        self.db.refresh(label_share)
        return label_share
    
    def remove_label_share(self, label_id: int, user_id: int) -> None:
        self.db.exec(
            delete(LabelShare)
            .where(LabelShare.label_id == label_id, LabelShare.user_id == user_id)
        )
        self.db.commit()