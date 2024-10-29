from jwt import encode, decode, exceptions
from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from config.dot_env_config import JWT_SECRET_KEY, TOKEN_EXPIRE_MINUTES, ALGORITHM

def expire_date(minutes: int) -> datetime:
    return datetime.now() + timedelta(minutes=minutes)

def write_jwt(data: dict) -> dict:
    token = encode(payload={ **data, "exp": expire_date(TOKEN_EXPIRE_MINUTES) }, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_jwt(token, output=False):
    try:
        if output:
            return decode(token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        decode(token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=status.HTTP_401_UNAUTHORIZED)
