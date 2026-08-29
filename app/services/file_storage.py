import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile, status

MEDIA_DIR = "app/media"
ALLOW_MIME = ["image/png", "image/jpeg"]
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))  # Tamaño máximo de archivo en MB
CHUNKS = 1024 * 1024  # Tamaño del bloque de lectura en bytes (1 MB)

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
    
    # class _ChunkCounter:
    #     def __init__(self, f):
    #         self._f = f
    #         self.calls = 0
    #         self.sizes = []
    #     def read(self, n=-1):
    #         data = self._f.read(n)
    #         if data:
    #             self.calls += 1
    #             self.sizes.append(len(data))
    #         return data
    #     def __getattr__(self, name):  # delega cualquier otro atributo
    #         return getattr(self._f, name)

    # reader = _ChunkCounter(file.file)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, length=CHUNKS) # Copia el archivo en bloques de 1 MB para evitar problemas de memoria con archivos grandes
        # shutil.copyfileobj(reader, buffer, length=CHUNKS) # Con reader para ver los CHUNKS
        
    size = os.path.getsize(file_path)
    if size > MAX_MB * CHUNKS:
        os.remove(file_path)  # Elimina el archivo si excede el tamaño máximo
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo excede el tamaño máximo permitido de {MAX_MB} MB"
        )
        
    return {
        "filename": filename,
        "content_type": file.content_type,
        "url": f"media/{ filename }",
        # "size": size,
        # "chunk_size_used": CHUNKS,
        # "chunk_calls": reader.calls,
        # "chunk_sizes_samples": reader.sizes[:5]
    }