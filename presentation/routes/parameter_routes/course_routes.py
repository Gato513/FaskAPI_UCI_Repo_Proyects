from fastapi import Request, Form, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates

from services.parameter_service.course_service import fetch_all_courses, create_new_course, delete_course_by_id, get_courses_by_faculty, update_course
from services.parameter_service.career_service import fetch_all_careers

from config.database_config import get_db
from util.jwt_functions import get_current_user  # Importa get_current_user para autenticación

# Función para verificar que el usuario es administrador
def verify_admin(user):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

#@ Renderizar Paginas:
async def render_course_page(request: Request, db: Session, error: str = None):
    courses = await fetch_all_courses(db)  # Obtener todos los cursos.
    careers = await fetch_all_careers(db)  # Obtener todas las carreras.

    return templates.TemplateResponse(
        "parameter_management/courses.html",
        {"request": request, "courses": courses, "careers": careers, "error": error}
    )

#@ Renderizar Cursos:
@router.get("/course")
async def show_course(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    return await render_course_page(request, db)

#() Crear Cursos:
@router.post("/course")
async def crear_course(
    request: Request,
    course_name: str = Form(...),
    career_id: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await create_new_course(course_name, career_id, db)
        return await render_course_page(request, db)
    except HTTPException as e:
        return await render_course_page(request, db, error=e)

#! Eliminar Curso:
@router.get("/delete/course/{course_id}")
async def delete_course(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await delete_course_by_id(course_id, db)
        return RedirectResponse(url="/dashboard/parameters/course", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        return await render_course_page(request, db, error=e)

#? Actualizar Curso:
@router.post("/update/course/{course_id}")
async def edit_course(
    request: Request,
    course_id: int,
    course_name: str = Form(...),
    career_id: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        await update_course(course_id, course_name, career_id, db)
        return RedirectResponse(url="/dashboard/parameters/course", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_course_page(request, db, error=e)

#% Retornar cursos filtrados
@router.get("/courses_by_faculty/{faculty_id}")
async def get_courses_by_faculty_id(
    faculty_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    verify_admin(user)  # Verificar que el usuario sea administrador
    try:
        courses = await get_courses_by_faculty(faculty_id, db)
        return {"status_code": 200, "courses": courses}
    except HTTPException as e:
        return {"status_code": e.status_code, "error_detail": e.detail}




