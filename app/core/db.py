import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")
print("Conectado a: ", DATABASE_URL)

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = { "check_same_thread": False }

# 1. Motor de base de datos
# create_engine crea un motor de base de datos que gestiona la conexión a la base de datos.
engine = create_engine(
    DATABASE_URL, 
    echo=False,         # Ponlo en True solo en desarrollo si quieres ver el SQL crudo
    pool_size=5,        # Mantiene 5 conexiones listas
    max_overflow=10,    # Permite crear 10 más si hay un pico de tráfico
    future=True, **engine_kwargs
)

# 2. Fábrica de sesiones
# sessionmaker crea una clase configurada lista para instanciar sesiones.
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    class_=Session
)

class Base(DeclarativeBase):
    pass

# 3. Dependencia para obtener la sesión de base de datos
# Esta función se puede usar en FastAPI para inyectar la sesión de base de datos en las rutas.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()