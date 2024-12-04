from fastapi import Request, Depends
from config.database_config import get_db
from config.server_config import router, templates
from sqlalchemy.orm import Session
from data.audits_data_base import get_all_audits  # Asegúrate de importar la función de auditoría

@router.get("/show_audit_record")
async def show_audit_record(request: Request, db: Session = Depends(get_db)):
    # Obtener todas las auditorías de la base de datos
    audits = get_all_audits(db)
    
    # Pasar las auditorías a la plantilla
    return templates.TemplateResponse("audit_and_monitoring/show_audit_record.html", {
        "request": request,
        "audits": audits  # Pasar las auditorías para que puedan ser mostradas en la plantilla
    })
