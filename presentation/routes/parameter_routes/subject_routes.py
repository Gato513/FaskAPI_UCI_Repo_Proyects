from fastapi import Request, Form, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from services.parameter_service.subject_service import get_all_subject, create_new_subjec, delete_subject_by_id, update_subject
from services.parameter_service.faculty_service import fetch_all_faculties
from config.database_config import get_db
from util.jwt_functions import get_current_user  # Importar la autenticación JWT

# Función para verificar que el usuario es administrador
def verify_admin(user):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

#@ Renderizar Materias y Cursos
async def render_subjects_page(request: Request, db: Session, error: str = None):
    faculties = await fetch_all_faculties(db)  # Obtener todas las Facultades
    subjects = await get_all_subject(db)  # Obtener todas las materias.
    return templates.TemplateResponse(
        "parameter_management/subjects.html",
        {"request": request, "faculties": faculties, "subjects": subjects, "error": error}
    )

#@ Mostrar Materias:
@router.get("/subject")
async def show_subject(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    return await render_subjects_page(request, db)

#( Crear Materia:
@router.post("/subject")
async def crear_subject(
    request: Request,
    subjects_name: str = Form(...),
    id_course: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await create_new_subjec(subjects_name, id_course, db)
        return await render_subjects_page(request, db)
    except HTTPException as e:
        return await render_subjects_page(request, db, error=e)

#! Eliminar Materia:
@router.get("/delete/subject/{subject_id}")
async def delete_subject(
    request: Request,
    subject_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        # Eliminar la materia
        await delete_subject_by_id(subject_id, db)

        # Después de eliminar, renderizar la página actualizada
        return RedirectResponse(url="/dashboard/parameters/subject", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        return await render_subjects_page(request, db, error=e)

#? Actualizar Curso:
@router.post("/update/subject/{subject_id}")
async def edit_subject(
    request: Request,
    subject_id: int,
    subject_name: str = Form(...),
    id_course: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await update_subject(subject_id, subject_name, id_course, db)
        return RedirectResponse(url="/dashboard/parameters/subject", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        # Si hay un error, renderizar la página con el mensaje de error
        return await render_subjects_page(request, db, error=e)



