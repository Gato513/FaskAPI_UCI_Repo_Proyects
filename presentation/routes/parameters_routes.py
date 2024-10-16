from fastapi import Request
from config.server_config import router, templates

@router.get("/facultades")
async def show_facultades(request: Request):
    return templates.TemplateResponse("parameter_management/faculties.html", {"request": request})

@router.get("/carreras")
async def show_carreras(request: Request):
    return templates.TemplateResponse("parameter_management/racing.html", {"request": request})

@router.get("/cursos")
async def show_cursos(request: Request):
    return templates.TemplateResponse("parameter_management/courses.html", {"request": request})

@router.get("/materias")
async def show_materias(request: Request):
    return templates.TemplateResponse("parameter_management/subjects.html", {"request": request})
