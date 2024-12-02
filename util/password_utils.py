from passlib.context import CryptContext

# Configuración del contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para encriptar la contraseña
def hash_password(password: str, salt: str) -> str:
    """Combina la contraseña con el salt y genera un hash seguro."""
    return pwd_context.hash(password + salt)
