# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Materia
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#$ CRUD Basico:
#@ Función para obtener todas las materias:
def get_all(db: Session):
    try:
        subject_data = db.query(Materia).all()
        return subject_data
    
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#@ Función para obtener una Materia por id:
def subject_by_id(db: Session, subject_id: int):
    try:
        return db.query(Materia).filter(Materia.id_materia == subject_id).first()
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#@ Función para obtener una materias por id:
def get_by_id(db: Session, subject_id: int):
    try:
        return db.query(Materia).filter(Materia.id_materia == subject_id).first()
    
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#() Función para crear una materia:
def create_subject(db: Session, subject_name: str, id_course: int):
    try:
        new_subject = Materia(nombre_materia=subject_name, id_curso=id_course)
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
    
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#! Función para eliminar Materia:
def delete_by_id(subject, db: Session):
    try:
        db.delete(subject)  # Se pasa la instancia de la materia
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#? Actulizar Materia:
def update_subject_by_id(subject, subject_name: str, id_course: str, db: Session): 
    try:
        subject.nombre_materia = subject_name
        subject.id_curso = id_course
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")

#$ Validaciones de Dependencias:
#% Función para verificar si existen dependencias de cursos para una carrera
def check_subjects_dependencies(db: Session, course_id: int) -> bool:
    try:
        exists = db.query(Materia).filter(Materia.id_curso == course_id).first() is not None # Consulta si existen Cursos asociadas a la Materia
        return exists
    except SQLAlchemyError as e:
        db.rollback()  # Reversión en caso de fallo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")