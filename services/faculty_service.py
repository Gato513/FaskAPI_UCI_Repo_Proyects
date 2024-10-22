from passlib.context import CryptContext
from data.faculty_data_base import faculty_by_name, create_faculty, get_all, faculty_by_id, delete_by_id
from fastapi import HTTPException, status
from sqlalchemy.orm import Session



def faculty_validation(faculty_name: str, db: Session):
    faculty_exist = faculty_by_name(db, faculty_name) #! Verificar si la facultad ya existe en la base de datos

    # Si existe, lanzar una excepción con código 409 (conflicto)
    if faculty_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La facultad ya existe")
    
    return faculty_exist

async def get_all_faculties(db: Session): 
    return get_all(db)

async def create_new_faculty(new_faculty: str, db: Session) -> str:
    # Verificar si el nombre de la facultad está vacío
    if not new_faculty:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de Facultad")

    # Validar si la facultad ya existe
    faculty_validation(new_faculty, db)

    # Crear la nueva facultad
    create_faculty(db, new_faculty)
    
    # Retornar un mensaje de éxito
    return f"La facultad {new_faculty} ha sido creada exitosamente"

#? Eliminar facultad:
async def delete_faculty_by_id(faculty_id: int, db: Session):
    # Obtener la facultad por su ID
    faculty = faculty_by_id(db, faculty_id)
    
    # Verificar si la facultad existe
    if not faculty:
        raise HTTPException(status_code=404, detail="La facultad no existe")
    
    # Eliminar la facultad
    delete_by_id(faculty, db)  # Aquí se pasa la instancia del objeto, no solo el ID