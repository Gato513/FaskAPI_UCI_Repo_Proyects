from data.course_data_base import  create_course, get_all, course_by_id, delete_by_id
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#? Octener todas las carreras de la base de datos:
async def get_all_courses(db: Session): 
    return get_all(db)

#? Crear Nueva Carrera:
async def create_new_course(new_course: str, id_course: int, db: Session) -> str:
    # Verificar si el nombre del curso está vacío
    if not new_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de Curso")

    # Crear el nuevo curso
    create_course(db, new_course, id_course)
    
    # Retornar un mensaje de éxito
    return f"El curso {new_course} ha sido creada exitosamente"


#? Eliminar curso:
async def delete_course_by_id(course_id: int, db: Session):
    # Obtener el curso por su ID
    course = course_by_id(db, course_id)
    
    # Verificar si el curso existe
    if not course:
        raise HTTPException(status_code=404, detail="El curso no existe")
    
    # Eliminar el curso
    delete_by_id(course, db)  # Aquí se pasa el instancia del objeto, no solo el ID

