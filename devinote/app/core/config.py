from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60*24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    PROJECT_NAME: str = "Devinote"
    
    class Config:
        env_file = ".env"

settings = Settings()