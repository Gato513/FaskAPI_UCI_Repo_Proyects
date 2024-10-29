from data.subject_data_base import create_subject, get_all, get_by_id, delete_by_id, subject_by_id, update_subject_by_id
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#? Octener todas las materias de la base de datos:
async def get_all_subject(db: Session): 
    return get_all(db)

#? Crear Nueva Carrera:
async def create_new_subjec(new_subjects: str, id_course: int, db: Session) -> str:
    # Verificar si el nombre de la Materia está vacío

    if not new_subjects or not id_course.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Complete los Parametros de Creacion")

    # Crear la nuevo Materia
    create_subject(db, new_subjects, id_course)
    
    # Retornar un mensaje de éxito
    return f"El Materia {new_subjects} ha sido creada exitosamente"

#? Eliminar Materia:
async def delete_subject_by_id(subject_id: int, db: Session):
    # Obtener la materia por su ID
    subject = get_by_id(db, subject_id)
    
    # Verificar si la materia existe
    if not subject:
        raise HTTPException(status_code=404, detail="La materia no existe")
    
    # Eliminar la materia
    delete_by_id(subject, db)  # Aquí se pasa la instancia del objeto, no solo el ID


#? Editar Una Materia:
async def update_subject(subject_id: int, subject_name: str, id_course: str, db: Session):

    if not subject_name or not id_course.isdigit():
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Complete los Parametros de Edicion")

    subject = subject_by_id(db, subject_id)                                            # Obtener la Materia por su ID

    if not subject:                                                                  # Verificar si la Materia existe
        raise HTTPException(status_code=404, detail="La materia no existe")

    if subject.nombre_materia == subject_name and subject.id_carrera == id_course:       # Verificar si la actualizacion es nesesaria:
        raise HTTPException(status_code=404, detail="Los datos de la Materia estan actualizados")

    update_subject_by_id(subject, subject_name, id_course, db)