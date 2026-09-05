import os

class Settings():
    # Seguridad (Tokens JWT)
    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-prod")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
settings = Settings()