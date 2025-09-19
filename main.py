from fastapi import status
from starlette.responses import RedirectResponse
from presentation.routes import session_routes, projects_routes, audits_routes
from config.server_config import app
from presentation.routes.parameter_routes import career_routes, course_routes, faculty_routes, subject_routes
from presentation.routes import users_rutes 

#% Definir Rutas de Sesion:
app.include_router(session_routes.router, prefix="/session")

#% Definir Rutas de Gestion de proyectos:
app.include_router(projects_routes.router, prefix="/dashboard/projects")

#% Definir Rutas de Gestion de parametros:
app.include_router(faculty_routes.router, prefix="/dashboard/parameters")
app.include_router(career_routes.router, prefix="/dashboard/parameters")
app.include_router(course_routes.router, prefix="/dashboard/parameters")
app.include_router(subject_routes.router, prefix="/dashboard/parameters")

#% Definir Rutas de Gestion de Usuarios:
app.include_router(users_rutes.router, prefix="/dashboard/users")

#% Definir Rutas de Auditorias:
app.include_router(audits_routes.router, prefix="/dashboard/audits")


#% Ruta de prueba para asegurarse de que la aplicación está funcionando
@app.get("/")
async def read_root():
    return RedirectResponse(url="/session/login", status_code=status.HTTP_302_FOUND)
