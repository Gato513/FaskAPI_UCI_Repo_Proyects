# Capa de Lógica de Negocio (Servicios)
from passlib.context import CryptContext
from data.user_data_base import user_by_email
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from util.jwt_functions import write_jwt

# Configuración del contexto de encriptación
#! pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def login(email: str, password: str, db: Session, ) -> int: 

    def verificar_password(plain_password, hashed_password):
    #! return pwd_context.verify(plain_password, hashed_password)
        return (plain_password == hashed_password)

    def authenticate_user(db: Session, email: str, password: str):
        user_exists = user_by_email(db, email) # Llamamos a la capa de datos y buscamos un usuario por email

        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario o Contraseña incorrecta")

        if not verificar_password(password, user_exists.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o Contraseña incorrecta")
    
        return user_exists

    try:
        usuario_verificado = authenticate_user(db, email, password) # Autenticamos el usuario
        if not usuario_verificado:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticación fallida")

        # Crear JWT token
        jwt_data = {'user_id': usuario_verificado.id, 'user_role': usuario_verificado.role}
        return write_jwt(jwt_data)
    
    except HTTPException as e:
        raise e  # Propaga la excepción a la capa de presentación
