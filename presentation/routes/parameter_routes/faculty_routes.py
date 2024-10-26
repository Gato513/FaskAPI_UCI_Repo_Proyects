from fastapi import Request, Form, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from services.parameter_service.faculty_service import create_new_faculty, get_all_faculties, delete_faculty_by_id, edit_faculty
from config.database_config import get_db

#? Renderizar Facultades
async def render_faculties_page(request: Request, db: Session, error: str = None):
    faculties = await get_all_faculties(db)  # Obtener todas las facultades.
    
    return templates.TemplateResponse(
        "parameter_management/faculties.html",
        {"request": request, "faculties": faculties, "error": error}
    )

#? Renderizar Facultades:
@router.get("/faculty")
async def show_facultades(request: Request, db: Session = Depends(get_db)):
    return await render_faculties_page(request, db)


#? Crear Facultades:
@router.post("/faculty")
async def crear_faculty(request: Request, facutie_name: str = Form(...), db: Session = Depends(get_db)):
    try:
        await create_new_faculty(facutie_name, db)
        return await render_faculties_page(request, db)
    except HTTPException as e:
        return await render_faculties_page(request, db, error=e)


#? Eliminar Facultad y redirigir a la lista de Facultades actualizada:
@router.get("/delete/faculty/{faculty_id}")
async def delete_faculty(request: Request, faculty_id: int, db: Session = Depends(get_db)):
    try:
        # Eliminar la Facultad
        await delete_faculty_by_id(faculty_id, db)
        
        # Después de eliminar, simplemente renderizas la misma página con los datos actualizados
        return RedirectResponse(url="/dashboard/parameters/faculty", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_faculties_page(request, db, error=e.detail)


#? Actualizar Facultad y redirigir a la lista de Facultades actualizada:
@router.post("/update/faculty/{faculty_id}")
async def update_faculty(request: Request, faculty_id: int, facutie_name: str = Form(...), db: Session = Depends(get_db)):
    try:
        # Editar la Facultad
        await edit_faculty(faculty_id, facutie_name, db)
        
        # Después de Editar, simplemente renderizas la misma página con los datos actualizados
        return RedirectResponse(url="/dashboard/parameters/faculty", status_code=status.HTTP_302_FOUND)
    
    except HTTPException as e:
        # Si hay un error, igual renderizas la página con el mensaje de error
        return await render_faculties_page(request, db, error=e)