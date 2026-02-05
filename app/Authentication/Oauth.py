from jose import JWTError, jwt
from pydantic import EmailStr
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import os
from .. import schemas
# from sqlalchemy.orm import Session
# from . import schemas, database, models
# from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret Key
# Algorithm for encrypting token
# expiration time

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_acess_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    token_id: str = str(payload.get("name"))
    token_email: EmailStr = payload.get("email")

    if not token_id or not token_email:
        raise credentials_exception
    token_data = schemas.TokenData(id=token_id, email=token_email)
    return token_data