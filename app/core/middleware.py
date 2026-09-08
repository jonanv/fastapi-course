import time
from typing import Any

from fastapi import FastAPI, Request

def register_middleware(app: FastAPI) -> None:
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next) -> Any:
        start = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{process_time:.4f} s"
        return response