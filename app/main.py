import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.core.db import Base, engine
from app.api.v1.auth.router import router as auth_router
from app.api.v1.user.router import router as user_router
from app.api.v1.post.router import router as post_router
from app.api.v1.tag.router import router as tag_router
from app.api.v1.upload.router import router as upload_router

load_dotenv()

MEDIA_DIR = "app/media"

def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Application", 
        description="This is a sample FastAPI application.", 
        version="1.0.0"
    )
    Base.metadata.create_all(bind=engine) # dev
    
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(user_router)
    app.include_router(post_router)
    app.include_router(tag_router)
    app.include_router(upload_router)
    
    # Crea la carpeta media si no existe
    os.makedirs(MEDIA_DIR, exist_ok=True)
    # Monta la URL para los archivos estaticos
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
    
    return app

app = create_app()