from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Esto carga las variables de tu archivo .env

# JWT
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
TOKEN_EXPIRE_MINUTES = int(getenv("TOKEN_EXPIRE_MINUTES", 60))  # default 60 si no existe
ALGORITHM = getenv("ALGORITHM", "HS256")

# Para el admin
ADMIN_USERNAME = getenv("ADMIN_USERNAME")
ADMIN_PHONE = getenv("ADMIN_PHONE")
ADMIN_DOCUMENT = getenv("ADMIN_DOCUMENT")
ADMIN_ADDRESS = getenv("ADMIN_ADDRESS")
ADMIN_EMAIL = getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

# Base de Datos
SQLALCHEMY_DATABASE_URL = getenv("SQLALCHEMY_DATABASE_URL")


