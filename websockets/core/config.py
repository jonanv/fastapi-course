from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py está en devinote/app/core/config.py
# .env está en devinote/.env
BASE_DIR = Path(__file__).resolve().parent.parent  # sube 3 niveles: core -> app -> devinote

class Settings(BaseSettings):
    PROJECT_NAME: str = "Websockets"

    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env",
        extra="ignore",  # Ignora cualquier variable no declarada arriba
    )

settings = Settings()