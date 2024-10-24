# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Materia
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#* Función para obtener todas las materias:
def get_all(db: Session):
    try:
        subject_data = db.query(Materia).all()
        return subject_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener una materias por id:
def get_by_id(db: Session, subject_id: int):
    try:
        return db.query(Materia).filter(Materia.id_materia == subject_id).first()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener una materia por su nombre:
def subject_by_name(db: Session, subject_name: str):
    try:
        subject_data = db.query(Materia).filter(Materia.nombre_materia == subject_name).first()
        return subject_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para crear un curso:
def create_subject(db: Session, subject_name: str, id_course: int):
    try:
        new_subject = Materia(nombre_materia=subject_name, id_curso=id_course)
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#! Eliminar Materia:
def delete_by_id(subject, db: Session):
    try:
        db.delete(subject)  # Se pasa la instancia de la materia
        db.commit()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")
