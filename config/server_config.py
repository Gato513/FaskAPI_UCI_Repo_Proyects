import os
from fastapi import FastAPI, APIRouter
from middlewares.user_middleware import UserMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from contextlib import asynccontextmanager
from config.database_config import get_db
from data.user_data_base import create_admin_user
from sqlalchemy.orm import Session

from config.database_config import engine
from models.all_model import Base

from dotenv import load_dotenv
load_dotenv()

# Crear el manejador de lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = next(get_db())  # Crear la sesión de base de datos
    create_admin_user(db)  # Crear el usuario admin si no existe
    print("La aplicación está iniciando...")

    yield  # El resto de la aplicación continúa ejecutándose

    print("La aplicación está cerrando...")

# Crear la instancia de FastAPI con lifespan
app = FastAPI(lifespan=lifespan)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

#% Configura las rutas para archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de las plantillas Jinja2
templates = Jinja2Templates(directory="templates")


# Definir filtro para formatear fechas y registrarlo en las plantillas
def format_datetime(value, format="%d/%m/%Y %H:%M"):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value
templates.env.globals['date'] = format_datetime


# Crear y montar la carpeta de elementos estáticos
store_dir = os.path.join(os.getcwd(), "store")

#% Comprobar si la carpeta "store" existe, si no, crearla
if not os.path.exists(store_dir):
    os.makedirs(store_dir)
    print(f"Se ha creado la carpeta: {store_dir}")

#% Montar la carpeta 'store' como un directorio estático
app.mount("/store", StaticFiles(directory=store_dir), name="store")
