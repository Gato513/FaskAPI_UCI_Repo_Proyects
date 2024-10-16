from os import getenv

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
TOKEN_EXPIRE_MINUTES = int(getenv("TOKEN_EXPIRE_MINUTES"))
ALGORITHM = getenv("ALGORITHM")
