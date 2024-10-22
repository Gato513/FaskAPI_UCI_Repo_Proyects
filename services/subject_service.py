from data.subject_data_base import create_subject, get_all, get_by_id ,delete_by_id
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#? Octener todas las materias de la base de datos:
async def get_all_subject(db: Session): 
    return get_all(db)

#? Crear Nueva Carrera:
async def create_new_subjec(new_subjects: str, id_course: int, db: Session) -> str:
    # Verificar si el nombre de la Materia está vacío
    if not new_subjects:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de Materia")

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


