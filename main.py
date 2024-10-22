from presentation.routes import session_routes, projects_routes, users_rutes, audits_routes, faculty_routes, career_routes, course_routes, subject_routes
from config.server_config import app #! Configuraciones del servidor:


# Definir Rutas de Sesion:
app.include_router(session_routes.router, prefix="/session")

# Definir Rutas de Gestion de proyectos:
app.include_router(projects_routes.router, prefix="/dashboard/projects")

# Definir Rutas de Gestion de parametros:
app.include_router(faculty_routes.router, prefix="/dashboard/parameters")
app.include_router(career_routes.router, prefix="/dashboard/parameters")
app.include_router(course_routes.router, prefix="/dashboard/parameters")
app.include_router(subject_routes.router, prefix="/dashboard/parameters")

# Definir Rutas de Gestion de Usuarios:
app.include_router(users_rutes.router, prefix="/dashboard/users")

# Definir Rutas de Auditorias:
app.include_router(audits_routes.router, prefix="/dashboard/audits")

# Ruta de prueba para asegurarse de que la aplicación está funcionando
@app.get("/")
async def read_root():
    return {"message": "API de FastAPI en funcionamiento"}

#! Email: juan.perez@example.com 
#! Pasword: hashed_password