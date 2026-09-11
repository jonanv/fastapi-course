from fastapi import APIRouter, status

from ...models.label import Label, LabelCreate, LabelRead
from ...services.label_service import LabelService
from ...api.dependencies import CurrentUser, DBSession


router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/", response_model=list[Label], response_description="Listar etiquetas")
def list_labels(db: DBSession, user: CurrentUser) -> list[Label]:
    return LabelService(db).list(user.id)

@router.post("/", response_model=LabelRead, response_description="Crear etiqueta", status_code=status.HTTP_201_CREATED)
def create_label(payload: LabelCreate, db: DBSession, user: CurrentUser) -> Label:
    return LabelService(db).create(user.id, payload)

@router.delete("/{label_id}", response_description="Eliminar etiqueta", status_code=status.HTTP_200_OK)
def delete_note(label_id: int, db: DBSession, user: CurrentUser) -> dict[str, str]:
    LabelService(db).delete(user.id, label_id)
    return { "message": "Etiqueta eliminada" }