from fastapi import Request, Form, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse  # Importa RedirectResponse
from sqlalchemy.orm import Session
from config.server_config import router, templates
from services.session_service import login
from config.database_config import get_db

@router.get("/login")
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def user_login(response: Response, request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        token_jwt = await login(email, password, db)  # Llama a la capa de lógica de negocio para autenticar al usuario

        # Configurar cookie HttpOnly
        response.set_cookie(
            key="access_token", 
            value=f"{token_jwt}",
            httponly=True,       # HttpOnly para evitar acceso desde el frontend
            secure=False,         # Solo enviar en HTTPS (cambiar a True en producción)
            samesite="Strict",    # Previene envío en solicitudes entre sitios
            max_age=1800          # Tiempo de expiración de la cookie (30 minutos)
        )

        # Redirigir a /dashboard después de configurar la cookie
        return RedirectResponse(url="/dashboard/projects/show_project", status_code=status.HTTP_303_SEE_OTHER, headers=response.headers)

    except HTTPException as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e.detail})  # Manejo de errores generales
