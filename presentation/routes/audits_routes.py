from fastapi import Request
from config.server_config import router, templates

@router.get("/show_audit_record")
async def show_audit_record(request: Request):
    return templates.TemplateResponse("audit_and_monitoring/show_audit_record.html", {"request": request})


