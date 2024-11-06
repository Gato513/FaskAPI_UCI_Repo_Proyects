from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from functools import wraps

from sqlalchemy.exc import IntegrityError, OperationalError

class DBTransactionManager:
    @staticmethod
    def handle_transaction(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db: Session = kwargs.get('db')
            try:
                result = func(*args, **kwargs)
                return result
            except IntegrityError as e:
                if db:
                    db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error de integridad en la base de datos: {str(e.orig)}"
                )
            except OperationalError as e:
                if db:
                    db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error operativo en la base de datos: {str(e)}"
                )
            except SQLAlchemyError as e:
                if db:
                    db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error en la base de datos: {str(e)} en la función {func.__name__}"
                )
        return wrapper
