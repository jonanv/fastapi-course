from fastapi import APIRouter, status

from app.models.share import LabelShare, NoteShare, ShareRequest
from app.services.share_service import ShareService
from app.api.dependencies import CurrentUser, DBSession


router = APIRouter(prefix="/shares", tags=["Shares"])

@router.post("/notes/{note_id}", response_model=NoteShare, response_description="Compartir nota compartida", status_code=status.HTTP_201_CREATED)
def share_note(note_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser) -> NoteShare:
    share = ShareService(db).share_note(user.id, note_id, payload.target_user_id, payload.role)
    return {
        "id": share.id,
        "note_id": note_id,
        "user_id": payload.target_user_id,
        "role": share.role
    }

@router.delete("/notes/{note_id}", response_description="Eliminar nota compartida", status_code=status.HTTP_200_OK)
def unshare_note(note_id: int, target_user_id: int, db: DBSession, user: CurrentUser) -> dict[str, str]:
    ShareService(db).unshare_note(user.id, note_id, target_user_id)
    return { "message": "Nota compartida eliminada" }

@router.post("/labels/{label_id}", response_model=LabelShare, response_description="Compartir etiqueta compartida", status_code=status.HTTP_201_CREATED)
def share_label(label_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser) -> LabelShare:
    share = ShareService(db).share_label(user.id, label_id, payload.target_user_id, payload.role)
    return {
        "id": share.id,
        "label_id": label_id,
        "user_id": payload.target_user_id,
        "role": share.role
    }

@router.delete("/labels/{label_id}", response_description="Eliminar etiqueta compartida", status_code=status.HTTP_200_OK)
def unshare_label(label_id: int, target_user_id: int, db: DBSession, user: CurrentUser) -> dict[str, str]:
    ShareService(db).unshare_label(user.id, label_id, target_user_id)
    return { "message": "Nota compartida eliminada" }