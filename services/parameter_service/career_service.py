from data.career_data_base import create_career, get_all, career_by_id, delete_by_id
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#? Octener todas las carreras de la base de datos:
async def get_all_careers(db: Session): 
    return get_all(db)

#? Crear Nueva Carrera:
async def create_new_career(new_career: str, facutie_id: int, db: Session) -> str:
    # Verificar si la nombre de la Carrera está vacío
    if not new_career:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de Carrera")

    # Crear la nuevo Carrera
    create_career(db, new_career, facutie_id)
    
    # Retornar un mensaje de éxito
    return f"la Carrera {new_career} ha sido creada exitosamente"

#? Eliminar Carrera:
async def delete_career_by_id(career_id: int, db: Session):
    # Obtener la Carrera por su ID
    career = career_by_id(db, career_id)
    
    # Verificar si la Carrera existe
    if not career:
        raise HTTPException(status_code=404, detail="La carrera no existe")
    
    # Eliminar la Carrera
    delete_by_id(career, db)  # Aquí se pasa la instancia del objeto, no solo el ID