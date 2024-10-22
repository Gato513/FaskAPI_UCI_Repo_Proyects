# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Facultad
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#* Función para obtener todas las facultades:
def get_all(db: Session):
    try:
        faculties_data = db.query(Facultad).all()
        return faculties_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener facultad por su nombre:
def faculty_by_name(db: Session, faculty_name: str):
    try:
        faculty_data = db.query(Facultad).filter(Facultad.nombre_facultad == faculty_name).first()
        return faculty_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para obtener una facultad por su id:
def faculty_by_id(db: Session, id_facultad: str):
    try:
        return db.query(Facultad).filter(Facultad.id_facultad == id_facultad).first()
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#* Función para crear una facultad
def create_faculty(db: Session, faculty_name: str):
    try:
        new_faculty = Facultad(nombre_facultad=faculty_name)
        db.add(new_faculty)
        db.commit()
        db.refresh(new_faculty)
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#! Eliminar Materia:
def delete_by_id(faculty, db: Session):
    try:
        db.delete(faculty)  # Se pasa la instancia de la materia
        db.commit()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")