"""Importaciones de FastAPI"""
from fastapi import FastAPI, WebSocket

from core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="This is a sample FastAPI application.", 
        version="1.0.0"
    )
    
    @app.websocket("/ws/echo")
    async def websocket_echo(websocket: WebSocket):
        """"Función que maneja los websockets"""
        await websocket.accept()
        
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: { data }")
    
    return app

app = create_app()