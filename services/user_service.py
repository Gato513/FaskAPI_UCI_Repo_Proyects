from data.user_data_base import (
    create_user,
    get_user_by_id,
    delete_user,
    get_all_faculties
)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request, Depends
from models.all_model import Usuario
from util.password_utils import hash_password 
import secrets
from typing import List

from util.save_uploaded_file import save_cover_image




# Función para crear un nuevo usuario
def create_new_user(db: Session, user_data: dict):
    # Verificar que las contraseñas coincidan
    if user_data['password'] != user_data['confirm_password']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")

    # Validar facultad_id y asignar None si está vacío o es None
    if user_data.get("facultad_id") == "" or user_data.get("facultad_id") is None:
        user_data["facultad_id"] = None

    # Generar un salt único para el usuario
    salt = secrets.token_hex(32)

    # Encriptar la contraseña combinada con el salt
    user_data['password'] = hash_password(user_data['password'], salt)
    user_data['salt'] = salt

    # Eliminar confirm_password ya que no se guarda en la base de datos
    user_data.pop('confirm_password')
    document = user_data.pop("document")

    #% Escribir la imagen de portada en el servidor:
    user_data["user_profile_url"] = save_cover_image(document)

    # Crear el objeto Usuario
    new_user = Usuario(**user_data)
    return create_user(db, new_user)

# Función para actualizar un usuario
def update_existing_user(db: Session, user_id: int, updated_data: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Si las contraseñas están presentes, asegúrate de que coincidan
    new_password = updated_data.get('password')
    confirm_password = updated_data.get('confirm_password')

    if new_password or confirm_password:
        if new_password != confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")

        # Generar nuevo salt y encriptar la nueva contraseña
        salt = secrets.token_hex(32)
        user.password = hash_password(new_password, salt)  # Usa la función centralizada
        user.salt = salt
        
    # Actualizar otros campos si están presentes en updated_data
    for key, value in updated_data.items():
        if key not in ['password', 'confirm_password'] and value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Función para eliminar un usuario en la capa de servicio
def delete_user_by_id(db: Session, user_id: int):
    return delete_user(db, user_id)

# Función para obtener la lista de facultades
def get_faculties_list(db: Session):
    return get_all_faculties(db)

def get_users_list(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()  # Esto obtiene todos los usuarios

def get_user_details(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Asegúrate de que la facultad esté cargada junto con el usuario, si existe
    facultad_name = user.facultad.nombre_facultad if user.facultad else "No asignada"
    
    return user, facultad_name

