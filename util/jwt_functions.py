from jwt import encode, decode, exceptions
from fastapi import status, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from config.dot_env_config import JWT_SECRET_KEY, TOKEN_EXPIRE_MINUTES, ALGORITHM
from sqlalchemy.orm import Session
from data.user_data_base import get_user_by_id
from config.database_config import get_db

# Genera una fecha de expiración en UTC
def expire_date(minutes: int) -> datetime:
    """Genera una fecha de expiración para el token JWT en UTC."""
    return datetime.utcnow() + timedelta(minutes=minutes)

# Codifica un JWT
def write_jwt(data: dict) -> str:
    """Codifica el payload en un token JWT."""
    payload = {**data, "exp": expire_date(TOKEN_EXPIRE_MINUTES)}
    token = encode(payload=payload, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

# Valida un JWT y retorna su payload si es válido
def validate_jwt(token: str) -> dict:
    """Valida el token JWT y retorna el payload si es válido."""
    try:
        return decode(token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token no válido")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al procesar el token: {str(e)}")

# Clase para representar al usuario autenticado
class User:
    def __init__(self, user_id: int, role: str):
        self.id = user_id
        self.role = role


# Middleware para obtener el usuario autenticado
async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Obtiene el usuario autenticado basado en el token JWT."""
    token = request.cookies.get("access_token")  # Obtiene el token de las cookies
    if not token:
        raise HTTPException(status_code=401, detail="No se encontró el token de autenticación")

    try:
        # Decodifica el token
        payload = validate_jwt(token)
        user_id = payload.get("user_id")
        role = payload.get("user_role")

        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Token inválido: falta información del usuario")

        # Busca al usuario en la base de datos
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return User(user_id=user.id, role=user.role)

    except HTTPException as e:
        # Reeleva las excepciones HTTP
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al procesar el token: {str(e)}")
