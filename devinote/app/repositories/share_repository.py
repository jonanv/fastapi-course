from sqlmodel import Session, select, delete

from devinote.app.models.share import NoteShare


class ShareRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def upsert_note_share(self, note_id: int, user_id: int, role: str) -> NoteShare:
        share = self.db.exec(
            select(NoteShare)
            .where(NoteShare.note_id == note_id, NoteShare.user_id == user_id)
        ).first()
        
        if share:
            share.role = role
            self.db.add(share)
            self.db.flush()
            self.db.commit()
            self.db.refresh(share)
            return share
        
        share = NoteShare(note_id=note_id, user_id=user_id, role=role)
        self.db.add(share)
        self.db.flush()
        self.db.commit()
        self.db.refresh(share)
        return share
    
    def remove_note_share(self, note_id: int, user_id: int) -> None:
        self.db.exec(
            delete(NoteShare)
            .where(NoteShare.note_id == note_id, NoteShare.user_id == user_id)
        )
        self.db.commit()