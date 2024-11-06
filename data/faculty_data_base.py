# Capa de Acceso a Datos (Repositorio / Base de Datos)
from decorators.db_transaction_manager import DBTransactionManager
from models.all_model import Facultad
from sqlalchemy.orm import Session

#@ Función para obtener todas las facultades:
@DBTransactionManager.handle_transaction
def get_all_faculties(db: Session) -> Facultad:
    return db.query(Facultad).all()


#@ Función para obtener facultad por su nombre:
@DBTransactionManager.handle_transaction
def faculty_by_name(db: Session, faculty_name: str) -> Facultad:
    return db.query(Facultad).filter(Facultad.nombre_facultad == faculty_name).first()


#@ Función para obtener una facultad por su id:
@DBTransactionManager.handle_transaction
def faculty_by_id(db: Session, id_facultad: str) -> Facultad:
    return db.query(Facultad).filter(Facultad.id_facultad == id_facultad).first()


#( Función para crear una facultad
@DBTransactionManager.handle_transaction
def create_faculty(db: Session, faculty_name: str) -> Facultad:
    new_faculty = Facultad(nombre_facultad=faculty_name)
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty


#! Eliminar Facultad:
@DBTransactionManager.handle_transaction
def delete_faculty(faculty, db: Session):
    db.delete(faculty)
    db.commit()


#? Actulizar Facultad:
@DBTransactionManager.handle_transaction
def update_faculty(faculty, facutie_name: str, db: Session):  
    faculty.nombre_facultad = facutie_name
    db.commit()


#% Actulizar Facultad:
@DBTransactionManager.handle_transaction
def deactivate_faculty(faculty, db: Session):  
    faculty.is_activated = False
    db.commit()
