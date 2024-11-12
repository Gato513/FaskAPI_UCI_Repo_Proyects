from fastapi import UploadFile, File
from typing import List, Optional
from fastapi import Request, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.server_config import router, templates

from services.proyects_service  import(
    fetch_proyects,
    fetch_proyect_by_id,
    create_new_project,
    fetch_all_subjects,
    fetch_all_students,
    handle_association_aggregation
)

from data.faculty_data_base import get_all_faculties
from data.career_data_base import get_all_careers
from data.course_data_base import get_all_courses
from data.proyect_data_base import get_all_keywords

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

    proyecto = await fetch_proyect_by_id(id_proyect, db)

    return templates.TemplateResponse(
        "project_management/project_detail.html",
        {"request": request, "proyecto": proyecto, "error": error}
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

#@ Renderizar Pagina de Edicion de Asociaciones del Proyecto:
@router.get("/show_project_association_page/{id_proyect}")
async def show_project_association_page(request: Request, id_proyect: str, db: Session = Depends(get_db)):

    proyect =  await fetch_proyect_by_id(id_proyect, db)
    id_curso = proyect.id_curso

    subjects = await fetch_all_subjects(id_curso, db)
    students = await fetch_all_students(id_curso, db)

    return templates.TemplateResponse(
        "project_management/edit_project_association.html",
        {"request": request, "id_proyect": id_proyect, "subjects": subjects, "students": students}
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


#$ Funcion para crear asociaciones a un Proyecto:
@router.post("/add_project_association/{id_project}")
async def add_project_association(
    request: Request,
    id_project: int,
    subjects: List[int] = Form([]),  # Lista vacía como valor por defecto
    students: List[int] = Form([]),  # Lista vacía como valor por defecto
    documents: List[UploadFile] = File(None),  # None como valor por defecto
    db: Session = Depends(get_db)
):
    try:

        
        
        associated_data = {
            "id_project": id_project,
            "subjects": subjects,
            "students": students,
            "documents": documents,
        }

        await handle_association_aggregation(associated_data, db)

        return RedirectResponse(url=f"/dashboard/projects/proyect_details/{id_project}", status_code=status.HTTP_302_FOUND)

    except HTTPException as e:
        print(e)
        return RedirectResponse(url=f"/dashboard/projects/add_project_association/{id_project}", status_code=status.HTTP_302_FOUND)
