from passlib.context import CryptContext
from data.faculty_data_base import faculty_by_name, create_faculty, all_faculties, faculty_by_id, delete_faculty, update_faculty, deactivate_faculty
from data.career_data_base import check_career_dependencies
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def faculty_validation(message: str, faculty_name: str, db: Session):
    faculty_exist = faculty_by_name(db, faculty_name) #! Verificar si la facultad ya existe en la base de datos

    # Si existe, lanzar una excepción con código 409 (conflicto)
    if faculty_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)
    
    return faculty_exist

#@ Octener todas las Facultades de la base de datos:
async def get_all_faculties(db: Session): 
    return all_faculties(db)

#$ Crear Nueva Facultad:
async def create_new_faculty(new_faculty: str, db: Session) -> str:
    # Verificar si el nombre de la facultad está vacío
    if not new_faculty:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de Facultad")

    # Validar si la facultad ya existe
    message = "La facultad ya existe"
    faculty_validation(message, new_faculty, db)

    # Crear la nueva facultad
    create_faculty(db, new_faculty)
    
    # Retornar un mensaje de éxito
    return f"La facultad {new_faculty} ha sido creada exitosamente"

#! Eliminar facultad:
async def delete_faculty_by_id(faculty_id: int, db: Session):
    # Obtener y verificar si la facultad existe
    faculty = faculty_by_id(db, faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La facultad no existe"
        )
    
    # Verificar si existen dependencias activas con carreras
    if check_career_dependencies(db, faculty_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Esta facultad no se puede eliminar. Existe una relación activa con carrera. Elimine primero la relación."
        )
    
    # Proceder a eliminar la facultad
    delete_faculty(faculty, db)

#? Editar Una facultad:
async def edit_faculty(faculty_id: int, facuty_name: str, db: Session):

    # Verificar si el nombre de la facultad está vacío
    if not facuty_name:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Complete los parametros de Edicion")

    # Validar si la facultad ya existe
    message = "El nombre de facultad ya existe. Si no selista esta desactivada."
    faculty_validation(message, facuty_name, db)
    
    # Obtener la facultad por su ID
    faculty = faculty_by_id(db, faculty_id)
    
    # Verificar si la facultad existe
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La facultad no existe")

    # Verificar si la actualizacion es nesesaria:
    if faculty.nombre_facultad == facuty_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Los datos de la Facultad estan actualizados")
    
    # acutualizar la facultad la facultad
    update_faculty(faculty, facuty_name, db)  # Aquí se pasa la instancia del objeto, no solo el ID

#% Desactivar Facultad:
async def deactivate_faculty_by_id(faculty_id: int, db: Session):
    # Obtener la facultad por su ID
    faculty = faculty_by_id(db, faculty_id)

    # Verificar si la facultad existe
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La facultad no existe")

    # Desactivar Facultad:
    deactivate_faculty(faculty, db)