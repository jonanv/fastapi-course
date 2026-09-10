from datetime import datetime, timedelta
import jwt
from pwdlib import PasswordHash

from .config import settings


password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Genera un hash seguro para la contraseña proporcionada."""
    return password_hash.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
    return password_hash.verify(plain, hashed)

def create_access_token(data: dict, minutes: int | None = None) -> str:
    """Crea un token JWT con los datos proporcionados y un tiempo de expiración opcional."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({ "exp": expire })
    return jwt.enconde(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    """Decodifica un token JWT y devuelve su contenido como un diccionario."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])