from typing import List, Optional
from fastapi import Request, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.server_config import router, templates
from services.proyects_service  import  fetch_proyects, fetch_proyect_by_id, create_new_project

from data.proyect_data_base import get_all_keywords
from data.faculty_data_base import get_all_faculties
from data.career_data_base import get_all_careers
from data.course_data_base import get_all_courses

from config.database_config import get_db

#& Renderizar Pagina de Proyectos:
async def render_show_page(request: Request, db: Session, error: str = None):

    proyects = await fetch_proyects(db)  # Obtener todas los pryectos.

    return templates.TemplateResponse(
        "project_management/show_project.html",
        {"request": request, "proyects": proyects, "error": error}
    )

#& Renderizar Pagina de Detalles
async def render_detail_page(request: Request, id_proyect: str, db: Session, error: str = None):

    proyect = await fetch_proyect_by_id(id_proyect, db)

    return templates.TemplateResponse(
        "project_management/project_detail.html",
        {"request": request, "proyect": proyect, "error": error}
    )

#& Renderizar Pagina de Creacion de Proyecto:
async def render_create_project_page(request: Request, db: Session, error: str = None):

    faculties = get_all_faculties(db)
    carers = get_all_careers(db)
    courses = get_all_courses(db)
    keywords = get_all_keywords(db)

    return templates.TemplateResponse(
        "project_management/create_project.html",
        {"request": request, "faculties": faculties, "carers": carers, "courses": courses, "keywords": keywords, "error": error}
    )


#@ Renderizar Lista de Proyectos:
@router.get("/show_project")
async def show_career(request: Request, db: Session = Depends(get_db)):
    return await render_show_page(request, db)

#@ Renderizar Detalles de un Proyecto:
@router.get("/proyect_details/{id_proyect}")
async def show_career(request: Request, id_proyect: str, db: Session = Depends(get_db)):
    try:
        return await render_detail_page(request, id_proyect, db)
    except HTTPException as e:
        return await render_detail_page(request, id_proyect, db, error=e)

#@ Renderizar Pagina de Creacion de proyectos:
@router.get("/create_project")
async def show_create_projects(request: Request, db: Session = Depends(get_db)):
    return await render_create_project_page(request, db)

#@ Renderizar Pagina de Edicion de proyectos:
@router.get("/edit_project/{id_proyect}")
async def show_projects_edit(request: Request, id_proyect: str, db: Session = Depends(get_db)):

    proyect = await fetch_proyect_by_id(id_proyect, db)

    return templates.TemplateResponse(
        "project_management/project_edit.html",
        {"request": request, "proyect": proyect}
    )


#$ Funcion para Crear un Nuevo Proyecto:
@router.post("/create_project")
async def crear_project(
    request: Request,
    nombre_proyecto: str = Form(...),
    descripcion_proyecto: str = Form(...),
    facultad_id: str = Form(...),
    carrera_id: str = Form(...),
    curso_id: str = Form(...),
    palabras_clave: Optional[List[str]] = Form(None),
    nueva_palabra_clave: str = Form(""),
    db: Session = Depends(get_db)
):

    #$ Asegurarse de que palabras_clave sea una lista vacía si no se proporciona:
    palabras_clave = palabras_clave or []

    try:
        project_data = {
            "nombre_proyecto": nombre_proyecto,
            "descripcion_proyecto": descripcion_proyecto,
            "facultad_id": facultad_id,
            "carrera_id": carrera_id,
            "curso_id": curso_id,
            "palabras_clave": palabras_clave,
            "nueva_palabra_clave": nueva_palabra_clave,
        }

        await create_new_project(project_data, db)

        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_302_FOUND)

    except HTTPException as e:
        return await render_create_project_page(request, db, error = e)


@router.get("/designated_project")
async def show_designated_projects(request: Request):
    return templates.TemplateResponse("project_management/designated_projects.html", {"request": request})

