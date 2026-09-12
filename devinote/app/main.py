from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.api.routers.auth_router import router as auth_router
from app.api.routers.note_router import router as note_router
from app.api.routers.label_router import router as label_router
from app.api.routers.share_router import router as share_router
from app.core.config import settings


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan,
        description="This is a sample FastAPI application.", 
        version="1.0.0",
        swagger_ui_parameters={
            "persistAuthorization": True
        }
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],    # Permitir todos los origines
        allow_credentials=True, # Permitir credenciales
        allow_methods=["*"],    # Permitir todos los métodos
        allow_headers=["*"]     # Permitir todos los headers
    )
    
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(note_router, prefix="/api/v1")
    app.include_router(label_router, prefix="/api/v1")
    app.include_router(share_router, prefix="/api/v1")
    
    return app

app = create_app()