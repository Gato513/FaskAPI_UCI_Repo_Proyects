from fastapi import Request
from config.server_config import router, templates

#! Rutas para renderizar HTML
@router.get("/show_project")
async def show_projects_list(request: Request):
    return templates.TemplateResponse("project_management/show_project.html", {"request": request})

@router.get("/create_project")
async def show_create_projects(request: Request):
    return templates.TemplateResponse("project_management/create_project.html", {"request": request})

@router.get("/modify_project")
async def show_projects_modify(request: Request):
    return templates.TemplateResponse("project_management/modify_project.html", {"request": request})

@router.get("/designated_project")
async def show_designated_projects(request: Request):
    return templates.TemplateResponse("project_management/designated_projects.html", {"request": request})

