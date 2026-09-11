from fastapi import HTTPException, status
from sqlmodel import Session

from ..models.share import NoteShare, ShareRole
from ..repositories.label_repository import LabelRepository
from ..repositories.note_repository import NoteRepository
from ..repositories.share_repository import ShareRepository


class ShareService:
    def __init__(self, db: Session):
        self.shares = ShareRepository(db)
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)
    
    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole) -> NoteShare:
        note = self.notes.get_by_id(note_id)
        
        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada o no autorizado")
        
        share = self.shares.upsert_note_share(note_id, target_user_id, role.value if hasattr(role, "value") else role)
        
        return share
    
    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int) -> None:
        note = self.notes.get_by_id(note_id)
                
        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada o no autorizado")
        
        self.shares.remove_note_share(note_id, target_user_id)
    
    