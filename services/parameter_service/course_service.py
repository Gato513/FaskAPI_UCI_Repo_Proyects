from data.course_data_base import  create_course, get_all_courses, courses_by_faculty, course_by_id, delete_by_id, update_course_by_id
from data.subject_data_base import check_subjects_dependencies
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#@ Octener todas las Cursos de la base de datos:
async def fetch_all_courses(db: Session): 
    return get_all_courses(db)


#@ Octener todas las Cursos filtrado por facultad:
async def get_courses_by_faculty(faculty_id: int, db: Session):
    # Realiza la consulta para obtener los cursos filtrados por el id de la facultad
    result = courses_by_faculty(db, faculty_id) 
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facultad Sin Cursos")

    courses = []
    
    for course in result:
        data_curse = {
            "id_curso": course.id_curso,
            "nombre_curso": course.nombre_curso,
            "nombre_carrera": course.carrera.nombre_carrera
        }
        courses.append(data_curse)

    return courses


#() Crear Nueva Curso:
async def create_new_course(new_course: str, career_id: int, db: Session) -> str:

    if not new_course or career_id == "Carreras":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Complete los Parametros de Creacion")

    create_course(db, new_course, career_id)

    return f"El curso {new_course} ha sido creada exitosamente"

#! Eliminar curso:
async def delete_course_by_id(course_id: int, db: Session):

    # Obtener y verificar si la carrera existe:
    course = course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El curso no existe"
        )
    
    # Verificar si existen dependencias activas con materias
    if check_subjects_dependencies(db, course_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Este curso no se puede eliminar. Existe una relación activa con materias. Elimine primero la relación."
        )
    
    # Eliminar el curso de la DB:
    delete_by_id(course, db)


#? Editar Una Curso:
async def update_course(course_id: int, course_name: str, career_id: str, db: Session):

    if not course_name or career_id == "Carreras":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Complete los Parametros de Edicion")

    course = course_by_id(db, course_id)                                            # Obtener la curso por su ID

    if not course:                                                                  # Verificar si la curso existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El curso no existe")

    if course.nombre_curso == course_name and course.id_carrera == career_id:       # Verificar si la actualizacion es nesesaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Los datos del curso estan actualizados")

    update_course_by_id(course, course_name, career_id, db)