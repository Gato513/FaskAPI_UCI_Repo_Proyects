from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config.database_config import engine
from models.all_model import Base

from dotenv import load_dotenv
load_dotenv() # Cargar las variables desde el archivo .env

# Creación del Instancia y enrutador de FastAPI
app = FastAPI()
router = APIRouter()
Base.metadata.create_all(bind=engine)

# Configura las rutas para archivos estáticos
# Monta el directorio "static" en la URL "/static" para que los archivos estáticos (CSS, JS, imágenes) estén disponibles públicamente
app.mount("/static", StaticFiles(directory="static"), name="static")


# Configuración de las plantillas Jinja2
#? Define el directorio donde se almacenarán las plantillas HTML
templates = Jinja2Templates(directory="templates")


