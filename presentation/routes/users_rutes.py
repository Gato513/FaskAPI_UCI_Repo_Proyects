from fastapi import HTTPException, Request, Depends, Form, status
from starlette.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from config.database_config import get_db
from data.user_data_base import check_field_uniqueness, get_user_by_id
from services.user_service import (
    create_new_user, 
    delete_user_by_id, 
    get_faculties_list, 
    get_user_details, 
    get_users_list, 
    update_existing_user
)
from util.jwt_functions import get_current_user, User
from typing import Optional


@router.get("/show_users")
async def show_users_list(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    users = get_users_list(db)
    if user.role == "admin":
        users = [u for u in users if u.id != user.id and u.role in ["profesor", "alumno"]]
    elif user.role == "profesor":
        users = [u for u in users if u.role == "alumno"]
    else:
        raise HTTPException(status_code=403, detail="No tiene permisos para ver usuarios")
    
    print(users)

    return templates.TemplateResponse("/user_management/show_users.html", {"request": request, "users": users})


@router.get("/create_user")
async def show_users_create(
    request: Request, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para crear usuarios")
    faculties = get_faculties_list(db)
    return templates.TemplateResponse(
        "/user_management/create_user.html", 
        {"request": request, "faculties": faculties, "user": user}
    )


@router.post("/create_user")
async def create_user_route(
    user_name: str = Form(...),
    user_phone: str = Form(...),
    user_document: str = Form(...),
    user_address: str = Form(...),
    user_matricula: Optional[str] = Form(None),
    user_email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(...),
    facultad_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para crear usuarios")
    
    user_data = {
        "user_name": user_name,
        "user_phone": user_phone,
        "user_document": user_document,
        "user_address": user_address,
        "user_matricula": user_matricula,
        "user_email": user_email,
        "password": password,
        "confirm_password": confirm_password,
        "role": role,
        "facultad_id": facultad_id,
    }
    create_new_user(db, user_data)
    return RedirectResponse(url="/dashboard/users/show_users", status_code=303)


@router.get("/user_details/{user_id}")
async def show_user_details(
    request: Request, 
    user_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    user_details, facultad_name = get_user_details(db, user_id)
    if not user_details:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return templates.TemplateResponse("/user_management/user_details.html", {
        "request": request,
        "user": user_details,
        "facultad_name": facultad_name
    })


@router.get("/edit_user/{user_id}")
async def edit_user_form(
    request: Request, 
    user_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para editar usuarios")

    editing_user = get_user_by_id(db, user_id)
    if not editing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    facultades = get_faculties_list(db)
    return templates.TemplateResponse("user_management/edit_user.html", {
        "request": request,
        "user": user,
        "editing_user": editing_user,
        "facultades": facultades
    })


@router.post("/edit_user/{user_id}")
async def update_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    **user_data
):
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para editar usuarios")
    
    editing_user = get_user_by_id(db, user_id)
    if not editing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for field, value in user_data.items():
        if value is not None and getattr(editing_user, field) != value:
            check_field_uniqueness(db, field, value, user_id)
    update_existing_user(db, user_id, user_data)
    return RedirectResponse(url="/dashboard/users/show_users", status_code=303)


@router.post("/delete_user/{user_id}")
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No tiene permisos para eliminar usuarios")

    user_to_delete = get_user_by_id(db, user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    delete_user_by_id(db, user_id)
    return RedirectResponse(url="/dashboard/users/show_users", status_code=303)


@router.get("/profile")
async def show_profile(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("/profile_management/profile.html", {"request": request, "user": user})
