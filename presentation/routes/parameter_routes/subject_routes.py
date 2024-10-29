from fastapi import Request, Form, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from services.parameter_service.subject_service import get_all_subject, create_new_subjec, delete_subject_by_id, update_subject
from services.parameter_service.faculty_service import get_all_faculties
from config.database_config import get_db


#? Renderizar Materias y Cursos
async def render_subjects_page(request: Request, db: Session, error: str = None):
    faculties = await get_all_faculties(db)   # Obtener todas las Facultades
    subjects = await get_all_subject(db)     # Obtener todas las materias.
    return templates.TemplateResponse(
        "parameter_management/subjects.html",
        {"request": request, "faculties": faculties, "subjects": subjects, "error": error}
    )

#? Mostrar Materias:
@router.get("/subject")
async def show_subject(request: Request, db: Session = Depends(get_db)):
    return await render_subjects_page(request, db)


#? Crear Materia:
@router.post("/subject")
async def crear_subject(request: Request, subjects_name: str = Form(...), id_course: str = Form(...), db: Session = Depends(get_db)):
    try:
        await create_new_subjec(subjects_name, id_course, db)
        return await render_subjects_page(request, db)
    except HTTPException as e:
        return await render_subjects_page(request, db, error=e)


#? Eliminar Materia y redirigir a la lista de materias actualizada:
@router.get("/delete/subject/{subject_id}")
async def delete_subject(request: Request, subject_id: int, db: Session = Depends(get_db)):
    try:
        # Eliminar la materia
        await delete_subject_by_id(subject_id, db)
        
        # Después de eliminar, simplemente renderizas la misma página con los datos actualizados
        return RedirectResponse(url="/dashboard/parameters/subject", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_subjects_page(request, db, error=e)


#? Actualizar Curso y redirigir a la lista de Cursos actualizada:
@router.post("/update/subject/{subject_id}")
async def edit_subject(request: Request, subject_id: int, subject_name: str = Form(...), id_course: str = Form(...), db: Session = Depends(get_db)):

    try:
        await update_subject(subject_id, subject_name, id_course, db)
        return RedirectResponse(url="/dashboard/parameters/subject", status_code=status.HTTP_302_FOUND)

    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_subjects_page(request, db, error=e)