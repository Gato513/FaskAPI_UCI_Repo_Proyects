from sqlalchemy.orm import Session
from models.all_model import Auditoria
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime

# Obtener todas las auditorías
def get_all_audits(db: Session):
    try:
        return db.query(Auditoria).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener auditorías: {str(e)}"
        )

# Obtener auditorías por usuario
def get_audits_by_user(db: Session, user_id: int):
    try:
        return db.query(Auditoria).filter(Auditoria.usuario_id == user_id).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener auditorías para el usuario {user_id}: {str(e)}"
        )

# Registrar auditoría en la base de datos
def register_audit_entry(db: Session, descripcion: str, user_id: int, proyecto_id: int):
    try:
        nueva_auditoria = Auditoria(
            fecha_cambio=datetime.now(),
            descripcion_cambio=descripcion,
            usuario_id=user_id,
            proyecto_id=proyecto_id
        )
        db.add(nueva_auditoria)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar auditoría: {str(e)}"
        )
