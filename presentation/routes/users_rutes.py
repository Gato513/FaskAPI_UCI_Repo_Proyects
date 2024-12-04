from urllib import request
from fastapi import HTTPException, Request, Depends, Form, status
from starlette.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from config.database_config import get_db
from data.user_data_base import check_field_uniqueness
from services.user_service import create_new_user, delete_user_by_id, get_faculties_list, get_user_details, get_users_list, get_user_by_id, update_existing_user
from typing import Optional


@router.get("/show_users")
<<<<<<< HEAD
async def show_users_list(request: Request, db: Session = Depends(get_db)):
    # Obtener el usuario autenticado desde el estado
    user = getattr(request.state, "user", None)
=======
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
    
    for user in users:
        user.role = user.role.capitalize()
>>>>>>> 4099df07316ca1e990a8f6cfa469d3690e093235

    if not user:
        return HTMLResponse("Usuario no autenticado", status_code=401)

    # Verificar el rol del usuario autenticado y filtrar la lista de usuarios
    if user.role == "admin":
        # El admin puede ver profesores y alumnos, pero no a sí mismo
        users = get_users_list(db)
        users = [u for u in users if u.id != user.id and (u.role == "profesor" or u.role == "alumno")]
    elif user.role == "profesor":
        # El profesor solo puede ver alumnos
        users = get_users_list(db)
        users = [u for u in users if u.role == "alumno"]
    elif user.role == "alumno":
        # El alumno no puede ver ningún usuario
        return HTMLResponse("No tiene permisos para ver usuarios", status_code=403)
        
    # Renderizar la plantilla con los usuarios filtrados
    return templates.TemplateResponse("/user_management/show_users.html", {"request": request, "users": users})

@router.get("/create_user")
async def show_users_create(request: Request, db: Session = Depends(get_db)):
    user = getattr(request.state, "user", None)
    
    if not user:
        print("Usuario no autenticado.")
        return HTMLResponse("Usuario no autenticado", status_code=401)

    print(f"Usuario autenticado: {user.user_name}, Rol: {user.role}")
    if user.role == "alumno":
        return HTMLResponse("No tiene permisos para crear usuarios", status_code=403)

    faculties = get_faculties_list(db)
    return templates.TemplateResponse(
        "/user_management/create_user.html",
        {"request": request, "faculties": faculties, "user": user}
    )

# Endpoint POST para procesar la creación de un nuevo usuario
@router.post("/create_user")
async def create_user_route(
    user_name: str = Form(...),
    user_phone: str = Form(...),
    user_document: str = Form(...),
    user_address: str = Form(...),
    user_matricula: Optional[str] = Form(None),
    user_email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),  # Campo de confirmación de contraseña
    role: str = Form(...),
    facultad_id: Optional [int] = Form(None),  # Esto permite que facultad_id sea opcional
    db: Session = Depends(get_db)
):
    
    # Crear el diccionario con los datos del usuario
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

    # Llamar a la capa de servicio para procesar los datos
    create_new_user(db, user_data)

    # Redirigir a la página de la lista de usuarios
    return RedirectResponse(url="/dashboard/users/show_users", status_code=303)

@router.get("/user_details/{user_id}")
async def show_user_details(request: Request, user_id: int, db: Session = Depends(get_db)):
    # Obtener los detalles del usuario, incluida la facultad
    user, facultad_name = get_user_details(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Pasar los detalles del usuario y la facultad a la plantilla
    return templates.TemplateResponse("/user_management/user_details.html", {
        "request": request,
        "user": user,
        "facultad_name": facultad_name
    })

# Ruta para mostrar el formulario de edición de usuario
@router.get("/edit_user/{user_id}")
async def edit_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    # Usuario autenticado
    user = getattr(request.state, "user", None)
    if not user:
        return HTMLResponse("Usuario no autenticado", status_code=401)

    # Usuario que se está editando
    editing_user = get_user_by_id(db, user_id)
    if not editing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener la lista de facultades para el formulario
    facultades = get_faculties_list(db)
    
    return templates.TemplateResponse("user_management/edit_user.html", {
        "request": request,
        "user": user,  # Usuario autenticado
        "editing_user": editing_user,  # Usuario que se está editando
        "facultades": facultades
    })

# Ruta para procesar la edición del usuario
@router.post("/edit_user/{user_id}")
async def update_user(
    user_id: int,
<<<<<<< HEAD
    user_name: str = Form(None),  # Opcional
    user_phone: str = Form(None),  # Opcional
    user_document: str = Form(None),  # Opcional
    user_address: str = Form(None),  # Opcional
    user_matricula: str = Form(None),  # Opcional
    user_email: str = Form(None),  # Opcional
    password: str = Form(None),  # Opcional
    confirm_password: str = Form(None),  # Opcional
    role: str = Form(None),  # Opcional
    facultad_id: int = Form(None),  # Opcional
    db: Session = Depends(get_db)
):
    # Obtener el usuario que se quiere editar
=======
    user_name: str = Form(...),
    user_phone: str = Form(...),
    user_document: str = Form(...),
    user_address: str = Form(...),
    user_matricula: Optional[str] = Form(None),
    user_email: str = Form(...),
    password: Optional[str] = Form(None),
    confirm_password: Optional[str] = Form(None),
    role: str = Form(...),
    facultad_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Validar permisos
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para editar usuarios")

    # Validar existencia del usuario
>>>>>>> 4099df07316ca1e990a8f6cfa469d3690e093235
    editing_user = get_user_by_id(db, user_id)
    if not editing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

<<<<<<< HEAD
    # Validar unicidad solo si el campo ha cambiado
    if user_name and user_name != editing_user.user_name:
        check_field_uniqueness(db, "user_name", user_name, user_id)
    if user_phone and user_phone != editing_user.user_phone:
        check_field_uniqueness(db, "user_phone", user_phone, user_id)
    if user_document and user_document != editing_user.user_document:
        check_field_uniqueness(db, "user_document", user_document, user_id)
    if user_email and user_email != editing_user.user_email:
        check_field_uniqueness(db, "user_email", user_email, user_id)

    # Recolectar solo los campos modificados
    updated_data = {}
    if user_name:
        updated_data["user_name"] = user_name
    if user_phone:
        updated_data["user_phone"] = user_phone
    if user_document:
        updated_data["user_document"] = user_document
    if user_address:
        updated_data["user_address"] = user_address
    if user_matricula:
        updated_data["user_matricula"] = user_matricula
    if user_email:
        updated_data["user_email"] = user_email
    if password:
        updated_data["password"] = password  
    if role:
        updated_data["role"] = role
    if facultad_id:
        updated_data["facultad_id"] = facultad_id

    try:
        # Llamar al servicio para actualizar el usuario con los datos proporcionados
        update_existing_user(db, user_id, updated_data)

        # Redirigir a la lista de usuarios después de la actualización
        return RedirectResponse(url="/dashboard/users/show_users", status_code=303)

    except HTTPException as e:
        # Manejo de errores si algo sale mal durante la actualización
        return templates.TemplateResponse("user_management/edit_user.html", {
            "request": request,
            "user": editing_user,  # Pasar el usuario actual con los datos
            "facultades": get_faculties_list(db),  # Pasar las facultades disponibles
            "error": e.detail  # Mostrar el mensaje de error
        })
    
=======
    # Validar contraseñas (si aplica)
    if password and confirm_password and password != confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    # Preparar datos actualizados
    user_data = {
        "user_name": user_name,
        "user_phone": user_phone,
        "user_document": user_document,
        "user_address": user_address,
        "user_matricula": user_matricula,
        "user_email": user_email,
        "role": role,
        "facultad_id": facultad_id,
    }
    if password:
        user_data["password"] = password

    # Validar y actualizar usuario
    for field, value in user_data.items():
        if value is not None and getattr(editing_user, field) != value:
            check_field_uniqueness(db, field, value, user_id)

    update_existing_user(db, user_id, user_data)

    # Redireccionar al listado
    return RedirectResponse(url="/dashboard/users/show_users", status_code=303)


>>>>>>> 4099df07316ca1e990a8f6cfa469d3690e093235
@router.post("/delete_user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminar usuario
    delete_user_by_id(db, user_id)
    
    # Redirigir a la página de usuarios
    return RedirectResponse(url="/dashboard/users/show_users", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/profile")
async def show_profile(request: Request):
    return templates.TemplateResponse("/profile_management/profile.html",  {"request": request})
