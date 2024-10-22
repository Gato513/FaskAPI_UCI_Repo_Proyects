from fastapi import Request, Form, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates

from services.course_service import  get_all_courses, create_new_course, delete_course_by_id
from services.career_service  import  get_all_careers

from config.database_config import get_db

#? Renderizar Cursos:
async def render_course_page(request: Request, db: Session, error: str = None):
    courses = await get_all_courses(db) # Octener todos los cursos.
    careers = await get_all_careers(db) # Octener todas las carreras.

    return templates.TemplateResponse(
        "parameter_management/courses.html", 
        {"request": request, "courses": courses, "careers": careers, "error": error}
    )


#? Renderizar Cursos:
@router.get("/course")
async def show_course(request: Request, db: Session = Depends(get_db)):
    return await render_course_page(request, db)


#? Crear Carreras:
@router.post("/course")
async def crear_course(request: Request, course_name: str = Form(...), career_id: str = Form(...), db: Session = Depends(get_db)):
    try:
        await create_new_course(course_name, career_id, db)
        return await render_course_page(request, db)
    except HTTPException as e:
        return await render_course_page(request, db, error=e.detail)


#? Eliminar Curso y redirigir a la lista de Cursos actualizada:
@router.get("/delete/course/{course_id}")
async def delete_course(request: Request, course_id: int, db: Session = Depends(get_db)):
    try:
        # Eliminar la Curso
        await delete_course_by_id(course_id, db)
        
        # Después de eliminar, redireccionamos a la url de la pagian para rederizar los combios:
        return RedirectResponse(url="/dashboard/parameters/course", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, renderiza la página con el mensaje de error
        return await render_course_page(request, db, error=e.detail)