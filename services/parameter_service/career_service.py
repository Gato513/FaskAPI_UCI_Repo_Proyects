from data.career_data_base import create_career, get_all, career_by_id, career_by_name, delete_by_id, update_career_by_id
from data.course_data_base import check_course_dependencies
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def career_validation(career_name: str, db: Session):
    career_exist = career_by_name(db, career_name) #! Verificar si la facultad ya existe en la base de datos

    # Si existe, lanzar una excepción con código 409 (conflicto)
    if career_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La carrera ya existe")
    
    return career_exist

#@ Octener todas las carreras de la base de datos:
async def get_all_careers(db: Session): 
    return get_all(db)

#$ Crear Nueva Carrera:
async def create_new_career(new_career: str, facutie_id: str, db: Session) -> str:

    if not new_career or facutie_id == "Facultades":            # Verificar si el nombre de la Carrera o el id de la facultad está vacío:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Complete los Parametros de Creacion")

    career_validation(new_career, db)                           # Validar si la carrera ya existe

    create_career(db, new_career, facutie_id)

    return f"la Carrera {new_career} ha sido creada exitosamente"

#! Eliminar Carrera:
async def delete_career_by_id(career_id: int, db: Session):

    # Obtener y verificar si la carrera existe:
    career = career_by_id(db, career_id)
    if not career:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La carrera no existe"
        )
    
    # Verificar si existen dependencias activas con cursos
    if check_course_dependencies(db, career_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Esta carrera no se puede eliminar. Existe una relación activa con cursos. Elimine primero la relación."
        )

    delete_by_id(career, db)  

#? Editar Una carrera:
async def edit_career(career_id: int, career_name: str, facutie_id: str, db: Session): 

    if not career_name or facutie_id == "Facultades":                                           # Verificar si el nombre de la Carrera o el id de la facultad está vacío:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Complete los Parametros de Edicion")

    career = career_by_id(db, career_id)                                            # Obtener la carrera por su ID

    if not career:                                                                  # Verificar si la carrera existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La carrera no existe")

    if career.nombre_carrera == career_name and career.id_facultad == facutie_id:   # Verificar si la actualizacion es nesesaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Los datos de la carrera estan actualizados")

    update_career_by_id(career, career_name, facutie_id, db)

