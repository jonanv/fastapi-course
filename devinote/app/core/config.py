from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py está en devinote/app/core/config.py
# .env está en devinote/.env
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube 3 niveles: core -> app -> devinote

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60*24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    PROJECT_NAME: str = "Devinote"

    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env",
        # extra="ignore",  # Ignora cualquier variable no declarada arriba
    )

settings = Settings()