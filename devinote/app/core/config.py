from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py está en devinote/app/core/config.py
# .env está en devinote/.env
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube 3 niveles: core -> app -> devinote

class Settings(BaseSettings):
    database_engine: str = "sqlite"
    database_name: str = Field(env="DATABASE_NAME")
    database_user: str | None = Field(env="DATABASE_USER")
    database_pass: str | None = Field(env="DATABASE_PASS")
    database_host: str | None = Field(env="DATABASE_HOST")
    database_port: int | None = Field(env="DATABASE_PORT")
    
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60*24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    PROJECT_NAME: str = "Devinote"

    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env",
        extra="ignore",  # Ignora cualquier variable no declarada arriba
    )
    
    @property
    def DATABASE_URL(self) -> str:
        if self.database_engine == "sqlite" or self.database_engine == "":
            return "sqlite:///./devinote/devinote.db"
        return (
            f"{self.database_engine}://{self.database_user}:{self.database_pass}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

settings = Settings()