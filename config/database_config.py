from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos MySQL utilizando el driver pymysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:AA5606491@localhost/serveProyect"


# Creación del motor de conexión a la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica si la conexión está viva antes de usarla
    pool_size=10,        # Tamaño del pool de conexiones
    max_overflow=20      # Número máximo de conexiones extra
)

# Creación de la fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,  # No confirmar automáticamente las transacciones
    autoflush=False,   # No enviar cambios automáticos antes de las consultas
    bind=engine        # Asocia la sesión con el motor de conexión
)

# Base para los modelos de datos
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos en cada solicitud
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna la sesión de la base de datos para usarla en una solicitud
    finally:
        db.close()  # Cierra la sesión al finalizar la solicitud para liberar recursos
