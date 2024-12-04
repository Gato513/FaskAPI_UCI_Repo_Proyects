from fastapi import Request, Depends, HTTPException, status
from config.database_config import get_db
from config.server_config import router, templates
from sqlalchemy.orm import Session
from data.audits_data_base import get_all_audits  # Asegúrate de importar la función de auditoría
from util.jwt_functions import get_current_user  # Importar la autenticación JWT

# Función para verificar que el usuario sea admin o profesor
def verify_admin_or_teacher(user):
    if user.role not in ["admin", "profesor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

@router.get("/show_audit_record")
async def show_audit_record(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # Obtener el usuario autenticado
):
    # Verificar que el usuario sea admin o profesor
    verify_admin_or_teacher(user)

    # Obtener todas las auditorías de la base de datos
    audits = get_all_audits(db)
    
    # Pasar las auditorías a la plantilla
    return templates.TemplateResponse("audit_and_monitoring/show_audit_record.html", {
        "request": request,
        "audits": audits  # Pasar las auditorías para que puedan ser mostradas en la plantilla
    })


