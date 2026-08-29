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
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "filename": filename,
        "content_type": file.content_type,
        "url": f"media/{ filename }"
    }