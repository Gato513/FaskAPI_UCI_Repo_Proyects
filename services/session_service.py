# Capa de Lógica de Negocio (Servicios)
from passlib.context import CryptContext
from data.user_data_base import user_by_email
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from util.jwt_functions import write_jwt

# Configuración del contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar la contraseña con el salt
def verificar_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password + salt, hashed_password)

# Función para autenticar un usuario
def authenticate_user(db: Session, email: str, password: str):
    user = user_by_email(db, email)
    if not user or not verificar_password(password, user.salt, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrecta")
    return user

# Función para iniciar sesión y generar token JWT
async def login(email: str, password: str, db: Session) -> str:
    user = authenticate_user(db, email, password)
    jwt_data = {'user_id': user.id, 'user_role': user.role}
    return write_jwt(jwt_data)
