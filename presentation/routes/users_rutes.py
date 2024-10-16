from fastapi import Request
from config.server_config import router, templates

@router.get("/show_users")
async def show_users_list(request: Request):
    return templates.TemplateResponse("/user_management/show_users.html",  {"request": request})

@router.get("/create_user")
async def show_users_create(request: Request):
    return templates.TemplateResponse("/user_management/create_user.html", {"request": request})

@router.get("/profile")
async def show_profile(request: Request):
    return templates.TemplateResponse("/profile_management/profile.html",  {"request": request})