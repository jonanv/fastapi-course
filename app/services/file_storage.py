import os
import shutil
import uuid

from fastapi import File, HTTPException, UploadFile, status

MEDIA_DIR = "app/media"
ALLOW_MIME = ["image/png", "image/jpeg"]
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))  # Tamaño máximo de archivo en MB

def ensure_media_dir() -> None:
    # Crea la carpeta media si no existe
    os.makedirs(MEDIA_DIR, exist_ok=True)

def save_upload_image(file: UploadFile) -> dict[str, str]:
    if file.content_type not in ALLOW_MIME:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten imágenes PNG o JPEG"
        )
    
    ensure_media_dir()
    ext = os.path.splitext(file.filename)[1]
    filename = f"{ uuid.uuid4().hex }{ ext }"
    file_path = os.path.join(MEDIA_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, length=1024 * 1024) # Copia el archivo en bloques de 1 MB para evitar problemas de memoria con archivos grandes
        
    size = os.path.getsize(file_path)
    if size > MAX_MB * 1024 * 1024:
        os.remove(file_path)  # Elimina el archivo si excede el tamaño máximo
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo excede el tamaño máximo permitido de {MAX_MB} MB"
        )
        
    return {
        "filename": filename,
        "content_type": file.content_type,
        "url": f"media/{ filename }"
    }