import time
from typing import Any
import uuid

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware 


BLACKLIST = set([
    # "127.0.0.1"
])

def register_middleware(app: FastAPI) -> None:
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],    # Permitir todos los origines
        allow_credentials=True,
        allow_methods=["*"],    # Permitir todos los métodos
        allow_headers=["*"]     # Permitir todos los headers
    )
    
    # Middlewares personalizados
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next) -> Any:
        start = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{process_time:.4f} s"
        return response
    
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        print(f"***ENTRADA: { request.method } { request.url }***")
        response = await call_next(request)
        print(f"***SALIDA: { response.status_code }***")
        return response
    
    @app.middleware("http")
    async def add_request_id_header(request: Request, call_next):
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    
    @app.middleware("http")
    async def block_ip(request: Request, call_next):
        client_ip = request.client.host
        if client_ip in BLACKLIST:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado a esta IP")
        return await call_next(request)