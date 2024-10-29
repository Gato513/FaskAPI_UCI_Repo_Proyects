# Capa de Acceso a Datos (Repositorio / Base de Datos)
from models.all_model import Carrera
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#$ CRUD Basico:
#@ Función para obtener todas las carreras:
def get_all(db: Session):
    try:
        careers_data = db.query(Carrera).all()
        return careers_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#@ Función para obtener una carrera por id:
def career_by_id(db: Session, career_id: int):
    try:
        return db.query(Carrera).filter(Carrera.id_carrera == career_id).first()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#@ Función para obtener carrera por su nombre:
def career_by_name(db: Session, career_name: str):
    try:
        career_data = db.query(Carrera).filter(Carrera.nombre_carrera == career_name).first()
        return career_data
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#( Función para Crear Carrera:
def create_career(db: Session, career_name: str, facutie_id: int):
    try:
        new_career = Carrera(nombre_carrera=career_name, id_facultad=facutie_id)
        db.add(new_career)
        db.commit()
        db.refresh(new_career)
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#! Función para Eliminar Carrera:
def delete_by_id(career, db: Session):
    try:
        db.delete(career)  # Se pasa la instancia de la Carrera
        db.commit()
    
    except SQLAlchemyError as e:
        # Si ocurre algún error relacionado con la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")

#? Actulizar carrera:
def update_career_by_id(career, career_name: str, facutie_id: str, db: Session): 
    try:
        career.nombre_carrera = career_name
        career.id_facultad = facutie_id

        db.commit()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos") 


#$ Validaciones de Dependencias:
#% Función para verificar si existen dependencias de carrera para una facultad
def check_career_dependencies(db: Session, faculty_id: int) -> bool:
    try:
        exists = db.query(Carrera).filter(Carrera.id_facultad == faculty_id).first() is not None #? Consulta si existen carreras asociadas a la facultad
        return exists
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos")