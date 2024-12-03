import os
from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from config.database_config import engine
from models.all_model import Base

from dotenv import load_dotenv
load_dotenv()

#$ Creación del Instancia y enrutador de FastAPI
app = FastAPI()
router = APIRouter()
Base.metadata.create_all(bind=engine)

#% Configuración de las plantillas Jinja2
templates = Jinja2Templates(directory="templates")


#$ Definición del filtro para formatear fechas y registro del filtro usando el método `get_env()`
def format_datetime(value, format="%d/%m/%Y %H:%M"):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value
templates.env.globals['date'] = format_datetime


#$ Crear ruta de la carpeta de elementos:
store_dir = os.path.join(os.getcwd(), "store")

#$ Crea Ruta imágenes de portada:
static_covers_dir = os.path.join(os.getcwd(), "static", "project_covers")

#% Comprobar si la carpeta "store" existe, si no, crearla
if not os.path.exists(store_dir):
    os.makedirs(store_dir)
    print(f"Se ha creado la carpeta: {store_dir}")

#% Comprobar si el directorio para las portadas exista
if not os.path.exists(static_covers_dir):
    os.makedirs(static_covers_dir)
    print(f"Se ha creado la carpeta de portadas en: {static_covers_dir}")


#% Montar la carpeta 'store' como un directorio estático
app.mount("/store", StaticFiles(directory=store_dir), name="store")

#% Configura las rutas para archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")




