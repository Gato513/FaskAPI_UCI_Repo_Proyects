import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from config.database_config import get_db
from services.user_service import get_user_by_id
from config.dot_env_config import JWT_SECRET_KEY, ALGORITHM  # Asegúrate de que estos valores estén configurados en tu .env

class UserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        print(f"Token JWT recibido: {token}")

        if token:
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("user_id")
                user_role = payload.get("user_role")
                print(f"Decodificado JWT: user_id={user_id}, user_role={user_role}")

                # Crear la sesión manualmente
                db: Session = next(get_db())  # Obtén la sesión de la base de datos manualmente
                user = get_user_by_id(db, user_id)
                
                if user:
                    print(f"Usuario encontrado en la BD: {user.user_name}, Rol: {user.role}")
                    request.state.user = user
                else:
                    print(f"Usuario con ID {user_id} no encontrado en la BD.")
                    request.state.user = None
            except jwt.ExpiredSignatureError:
                print("Token expirado.")
                request.state.user = None
            except jwt.InvalidTokenError:
                print("Token no válido.")
                request.state.user = None
        else:
            print("Cookie 'access_token' no encontrada.")
            request.state.user = None

        response = await call_next(request)
        return response



