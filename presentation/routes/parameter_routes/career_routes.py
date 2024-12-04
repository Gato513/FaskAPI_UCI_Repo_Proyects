from fastapi import Request, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.server_config import router, templates
from services.parameter_service.career_service  import fetch_all_careers, create_new_career, delete_career_by_id, edit_career
from services.parameter_service.faculty_service import fetch_all_faculties
from config.database_config import get_db
from util.jwt_functions import get_current_user  # Importa get_current_user para autenticación

# Función para verificar que el usuario es administrador
def verify_admin(user):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

#@ Renderizar Materias y Cursos
async def render_careers_page(request: Request, db: Session, error: str = None):
    careers = await fetch_all_careers(db)  # Obtener todas las carreras.
    faculties = await fetch_all_faculties(db)  # Obtener todos las facultades.
    
    return templates.TemplateResponse(
        "parameter_management/career.html",
        {"request": request, "careers": careers, "faculties": faculties, "error": error}
    )

#@ Renderizar Carreras:
@router.get("/career")
async def show_career(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    return await render_careers_page(request, db)

#$ Crear Carreras:
@router.post("/career")
async def crear_career(
    request: Request,
    career_name: str = Form(...),
    facutie_id: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await create_new_career(career_name, facutie_id, db)
        return await render_careers_page(request, db)
    except HTTPException as e:
        return await render_careers_page(request, db, error=e)

#! Eliminar Materia y redirigir a la lista de materias actualizada:
@router.get("/delete/career/{career_id}")
async def delete_career(
    request: Request,
    career_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        # Eliminar la materia
        await delete_career_by_id(career_id, db)
        
        # Después de eliminar, simplemente renderizas la misma página con los datos actualizados
        return RedirectResponse(url="/dashboard/parameters/career", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_careers_page(request, db, error=e)

#? Actualizar Carrera y redirigir a la lista de Carreras actualizada:
@router.post("/update/career/{career_id}")
async def update_career(
    request: Request,
    career_id: int,
    career_name: str = Form(...),
    facutie_id: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        # Editar la Facultad
        await edit_career(career_id, career_name, facutie_id, db)
        
        # Después de Editar, simplemente renderizas la misma página con los datos actualizados
        return RedirectResponse(url="/dashboard/parameters/career", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_careers_page(request, db, error=e)




