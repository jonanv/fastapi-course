from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DBSession
from app.services.note_service import NoteService
from app.models.note import Note, NoteCreate, NoteRead, NoteUpdate


router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=list[NoteRead], response_description="Listar notas")
def list_notes(db: DBSession, user: CurrentUser) -> list[Note]:
    return NoteService(db).list_visible(user.id)

@router.post("/", response_model=NoteRead, response_description="Crear nota", status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: DBSession, user: CurrentUser) -> Note:
    return NoteService(db).create(user.id, payload)

@router.patch("/{note_id}", response_model=NoteRead, response_description="Actualizar nota", status_code=status.HTTP_200_OK)
def update_note(note_id: int, payload: NoteUpdate, db: DBSession, user: CurrentUser) -> Note:
    return NoteService(db).update(user.id, note_id, payload)

@router.delete("/{note_id}", response_description="Eliminar nota", status_code=status.HTTP_200_OK)
def delete_note(note_id: int, db: DBSession, user: CurrentUser) -> dict[str, str]:
    NoteService(db).delete(user.id, note_id)
    return { "message": "Nota eliminada" }