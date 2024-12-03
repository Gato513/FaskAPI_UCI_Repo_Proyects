from fastapi import Request, Form, Depends, HTTPException, status
from config.server_config import router, templates
from starlette.responses import RedirectResponse
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from services.proyects_service  import(
    fetch_proyects,
    fetch_proyect_by_id,
    create_new_project,
    fetch_all_subjects,
    fetch_all_students,
    handle_association_aggregation,
    delete_project_service, 
    delete_relation_service,
    update_project
)


from data.faculty_data_base import get_all_faculties
from data.proyect_data_base import get_all_keywords
from data.career_data_base  import get_all_careers
from data.course_data_base  import get_all_courses
from config.database_config import get_db


#& Renderizar Página de Proyectos con Filtros:
async def render_show_page(request: Request, db: Session, error: str = None):
    # Obtener parámetros de la solicitud
    query_params = request.query_params

    # Extraer filtros de los parámetros
    nombre_proyecto = query_params.get("nombre_proyecto", "").strip()
    facultad = query_params.get("facultad", "").strip()
    carrera = query_params.get("carrera", "").strip()
    curso = query_params.get("curso", "").strip()

    # Pasar filtros al servicio para obtener proyectos filtrados
    proyects = await fetch_proyects(
        db,
        nombre_proyecto=nombre_proyecto,
        facultad=facultad,
        carrera=carrera,
        curso=curso,
    )

    # Obtener listas para los selectores
    faculties = get_all_faculties(db)
    careers = get_all_careers(db)
    courses = get_all_courses(db)

    return templates.TemplateResponse(
        "project_management/show_project.html",
        {
            "request": request,
            "proyects": proyects,
            "faculties": faculties,
            "careers": careers,
            "courses": courses,
            "filters": {
                "nombre_proyecto": nombre_proyecto,
                "facultad": facultad,
                "carrera": carrera,
                "curso": curso,
            },
            "error": error,
        },
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

#@ Ruta para Mostrar Proyectos con Filtros
@router.get("/show_project")
async def show_projects(request: Request, db: Session = Depends(get_db)):
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

#@ Renderizar Página de Edición de Proyectos:
@router.get("/edit_project/{id_proyect}")
async def show_projects_edit(request: Request, id_proyect: str, db: Session = Depends(get_db)):
    try:
        proyect = await fetch_proyect_by_id(id_proyect, db)
        faculties = get_all_faculties(db)
        carers = get_all_careers(db)
        courses = get_all_courses(db)
        keywords = get_all_keywords(db)

        return templates.TemplateResponse(
            "project_management/project_edit.html",
            {
                "request": request,
                "project": proyect,
                "faculties": faculties,
                "carers": carers,
                "courses": courses,
                "keywords": keywords,
            }
        )
    except HTTPException as e:
        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_302_FOUND)

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


#$ Ruta para crear un nuevo proyecto
@router.post("/create_project")
async def crear_project(
    request: Request,
    nombre_proyecto: str = Form(...),
    descripcion_proyecto: str = Form(...),
    facultad_id: str = Form(...),
    carrera_id: str = Form(...),
    curso_id: str = Form(...),
    palabras_clave: List[int] = Form([]),
    nueva_palabra_clave: str = Form(""),
    document: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Datos del proyecto
    project_data = {
        "nombre_proyecto": nombre_proyecto,
        "descripcion_proyecto": descripcion_proyecto,
        "facultad_id": facultad_id,
        "carrera_id": carrera_id,
        "curso_id": curso_id,
        "palabras_clave": palabras_clave,
        "nueva_palabra_clave": nueva_palabra_clave,
        "document": document
    }

    try:
        # Crear el proyecto en la base de datos
        await create_new_project(project_data, db)

        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_302_FOUND)

    except HTTPException as e:
        # En caso de error, mostrar la página de creación del proyecto
        return await render_create_project_page(request, db, error=e)

#$ Funcion para crear asociaciones a un Proyecto:
@router.post("/add_project_association/{id_project}")
async def add_project_association(
    request: Request,
    id_project: int,
    subjects: List[int] = Form([]),  # Lista vacía como valor por defecto
    students: List[int] = Form([]),  # Lista vacía como valor por defecto
    documents: List[UploadFile] = File(None),  
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

#% Procesar Edición de Proyecto:
@router.post("/edit_project/{id_proyect}")
async def edit_project(
    request: Request,
    id_proyect: str,
    nombre_proyecto: str = Form(...),
    descripcion_proyecto: str = Form(...),
    facultad_id: str = Form(...),
    carrera_id: str = Form(...),
    curso_id: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # Construir los datos del proyecto
        project_data = {
            "id": id_proyect,
            "nombre_proyecto": nombre_proyecto,
            "descripcion_proyecto": descripcion_proyecto,
            "facultad_id": facultad_id,
            "carrera_id": carrera_id,
            "curso_id": curso_id,
        }

        # Procesar la actualización del proyecto
        await update_project(project_data, db)

        # Redirigir al listado de proyectos después de la actualización
        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_302_FOUND)

    except HTTPException as e:
        # Obtener datos necesarios para renderizar la página en caso de error
        proyect = await fetch_proyect_by_id(id_proyect, db)
        faculties = get_all_faculties(db)
        carers = get_all_careers(db)
        courses = get_all_courses(db)

        # Renderizar página con datos y error
        return templates.TemplateResponse(
            "project_management/project_edit.html",
            {
                "request": request,
                "project": proyect,
                "faculties": faculties,
                "carers": carers,
                "courses": courses,
                "error": str(e),
            },
        )

#! Ruta de eliminacion de proyectos y dependencias;
@router.get("/delete_proyect/{id_proyecto}")
async def delete_project(id_proyecto: int, db: Session = Depends(get_db)):
    try:
        await delete_project_service(id_proyecto, db)
        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        raise e


#! Ruta de eliminacion una relacion asociada al proyecto;
@router.get("/delete_relation/{id_proyecto}/{type_of_relation}/{id_relation}")
async def delete_relation(id_proyecto: int, type_of_relation: str, id_relation: int, db: Session = Depends(get_db)):
    try:
        await delete_relation_service(id_relation, type_of_relation, db)
        return RedirectResponse(url=f"/dashboard/projects/proyect_details/{id_proyecto}", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        raise e
