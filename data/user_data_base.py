# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Usuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

# Función para obtener el usuario por email
def user_by_email(db: Session, email: str):
    try:
        user_data = db.query(Usuario).filter(Usuario.user_email == email).first()
        return user_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")
