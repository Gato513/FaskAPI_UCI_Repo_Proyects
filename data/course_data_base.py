# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Curso
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#* Función para obtener todos los cursos:
def get_all(db: Session):
    try:
        courses_data = db.query(Curso).all()
        return courses_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener una curso por id:
def course_by_id(db: Session, course_id: int):
    try:
        return db.query(Curso).filter(Curso.id_curso == course_id).first()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener un curso por su nombre:
def course_by_name(db: Session, course_name: str):
    try:
        course_data = db.query(Curso).filter(Curso.nombre_curso == course_name).first()
        return course_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para crear un curso:
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
