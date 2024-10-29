# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Curso
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#$ CRUD Basico:
#@ Función para obtener todos los cursos:
def get_all(db: Session):
    try:
        return db.query(Curso).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#@ Función para obtener todos los cursos filtrados por id de la facultad:
def courses_by_faculty(db: Session, faculty_id: str):
    try:
        response = db.query(Curso).filter(Curso.carrera.has(id_facultad=faculty_id)).all()
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#@ Función para obtener una curso por id:
def course_by_id(db: Session, course_id: int):
    try:
        return db.query(Curso).filter(Curso.id_curso == course_id).first()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#@ Función para obtener un curso por su nombre:
def course_by_name(db: Session, course_name: str):
    try:
        course_data = db.query(Curso).filter(Curso.nombre_curso == course_name).first()
        return course_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#() Función para crear un curso:
def create_course(db: Session, course_name: str, id_course: int):
    try:
        new_course = Curso(nombre_curso=course_name, id_carrera=id_course)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#! Eliminar course:
def delete_by_id(course, db: Session):
    try:
        db.delete(course)  # Se pasa la instancia de la course
        db.commit()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#? Actulizar Curso:
def update_course_by_id(course, course_name: str, career_id: str, db: Session): 
    try:
        course.nombre_curso = course_name
        course.id_carrera = career_id
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos") 


#$ Validaciones de Dependencias:
#% Función para verificar si existen dependencias de cursos para una carrera
def check_course_dependencies(db: Session, career_id: int) -> bool:
    try:
        exists = db.query(Curso).filter(Curso.id_carrera == career_id).first() is not None # Consulta si existen Cursos asociadas a la Materia
        return exists
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")
