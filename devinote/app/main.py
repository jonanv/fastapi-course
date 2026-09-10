from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Application", 
        description="This is a sample FastAPI application.", 
        version="1.0.0",
        swagger_ui_parameters={
            "persistAuthorization": True
        }
    )
    
    @app.get("/")
    def read_root():
        return { "message": "Hello World" }
    
    return app

app = create_app()