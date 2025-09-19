# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Usuario, Facultad
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status 
from config.dot_env_config import ADMIN_USERNAME, ADMIN_PHONE, ADMIN_DOCUMENT, ADMIN_ADDRESS, ADMIN_EMAIL, ADMIN_PASSWORD
from util.password_utils import hash_password  # Importar desde util/password_utils
from secrets import token_hex  # Para generar el salt único


# Función para obtener el usuario por email
def user_by_email(db: Session, email: str):
    try:
        user_data = db.query(Usuario).filter(Usuario.user_email == email).first()
        return user_data
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

# Función para obtener usuario por ID
def get_user_by_id(db: Session, user_id: int):
    try:
        user_data = db.query(Usuario).filter(Usuario.id == user_id).first()
        if user_data:
            print(f"Usuario encontrado: {user_data.user_name}, Rol: {user_data.role}")
        else:
            print(f"No se encontró un usuario con ID: {user_id}")
        return user_data
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )

def create_user(db: Session, user: Usuario):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear usuario: {str(e)}")

# Función para actualizar usuario
def update_user(db: Session, user_id: int, updated_data: dict):
    try:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        for key, value in updated_data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar usuario: {str(e)}")

# Función para eliminar un usuario por ID
def delete_user(db: Session, user_id: int):
    try:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        db.delete(user)
        db.commit()
        return {"detail": "Usuario eliminado exitosamente"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar usuario: {str(e)}")

# Función para obtener todas las facultades
def get_all_faculties(db: Session):
    try:
        faculties = db.query(Facultad).all()
        return faculties
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")
    
def check_field_uniqueness(db: Session, field_name: str, field_value: str, user_id: int = None):
    try:
        # Validar solo si el valor no es None ni vacío
        if not field_value:
            return
        
        # Construir la consulta dinámicamente
        query = db.query(Usuario).filter(getattr(Usuario, field_name) == field_value)
        
        if user_id:
            query = query.filter(Usuario.id != user_id)  # Excluir el usuario actual
        
        existing_user = query.first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El campo '{field_name}' con valor '{field_value}' ya está en uso."
            )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar unicidad: {str(e)}"
        )

# Crear el usuario admin
def create_admin_user(db: Session):
    existing_admin = db.query(Usuario).filter(Usuario.role == "admin").first()
    if not existing_admin:
        # Leer las credenciales del archivo .env
        admin_name = ADMIN_USERNAME
        admin_phone = ADMIN_PHONE
        admin_document = ADMIN_DOCUMENT
        admin_address = ADMIN_ADDRESS
        admin_email = ADMIN_EMAIL
        admin_password = ADMIN_PASSWORD
        
        # Generar un salt único para el admin
        admin_salt = token_hex(32)  # Genera el salt
        hashed_password = hash_password(admin_password, admin_salt)  # Encripta la contraseña

        new_admin = Usuario(
            user_name=admin_name,
            user_phone=admin_phone,  # Usar valores desde .env
            user_document=admin_document,
            user_address=admin_address,  # Usar valores desde .env
            user_email=admin_email,
            password=hashed_password,
            salt=admin_salt,
            role="admin",
            user_profile_url="default_profile.png"  # <- Valor por defecto
        )
        
        try:
            db.add(new_admin)
            db.commit()
            print("Usuario admin creado exitosamente.")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error al crear el usuario admin: {e}")


