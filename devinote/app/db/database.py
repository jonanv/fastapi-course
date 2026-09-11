import os
from typing import Iterator
from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings


# Si la base de datos es SQLite, necesitamos pasar un argumento especial para permitir múltiples hilos.
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = { "check_same_thread": False }

# Motor de base de datos
# create_engine crea un motor de base de datos que gestiona la conexión a la base de datos.
engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,         # Ponlo en True solo en desarrollo si quieres ver el SQL crudo
    pool_size=5,        # Mantiene 5 conexiones listas
    max_overflow=10,    # Permite crear 10 más si hay un pico de tráfico
    future=True,        # Usa la nueva API de SQLAlchemy 2.0
    **engine_kwargs     # Pasa argumentos adicionales según el tipo de base de datos (por ejemplo, SQLite necesita check_same_thread=False)
)

# Crear todas las tablas en la base de datos, devuelve un objeto MetaData que contiene todas las tablas y relaciones definidas en tus modelos SQLModel. Luego, create_all() crea esas tablas en la base de datos si no existen.
def init_db() -> None:
    """Inicializa la base de datos creando todas las tablas definidas en los modelos SQLModel."""
    SQLModel.metadata.create_all(engine) # dev, solo para desarrollo

def get_session() -> Iterator[Session]:
    """Devuelve una sesión de base de datos. Úsalo con 'with' para asegurarte de que se cierre correctamente y automaticamente evitando fugas de conexión."""
    with Session(engine) as session:
        yield session