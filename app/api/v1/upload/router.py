from fastapi import APIRouter, File, HTTPException, UploadFile, status
from typing import Any

from app.services.file_storage import save_upload_image

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/bytes", response_model="", response_description="")
async def upload_bytes(file: bytes = File(...)) -> dict[str, Any]:
    return {
        "filename": "archivo_subido",
        "size_bytes": len(file)
    }

@router.post("/file", response_model="", response_description="")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str | None]:
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }
    
@router.post("/save", response_model="", response_description="")
async def save_file(file: UploadFile = File(...)) -> dict[str, str]:
    saved = save_upload_image(file)
        
    return {
        "filename": saved["filename"],
        "content_type": saved["content_type"],
        "url": saved["url"]
    }