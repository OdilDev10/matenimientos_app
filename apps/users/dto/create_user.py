import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from apps.users.models import Roles
from config.config import PWD_CONTEXT


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


class UserCreate(BaseModel):
    name: str
    last_name: str
    age: int
    email: str
    password: str
    role: Roles = Roles.CLIENT


class UserInDB(UserCreate):
    hashed_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    last_name: str
    age: str
    role: str


# Funciones auxiliares
def hash_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def create_jwt_token(email: str):
    expiration = datetime.now() + timedelta(hours=1)  # Token expira en 1 hora
    token = jwt.encode(
        {"sub": email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM
    )
    return token

def decode_jwt_token(token: str):
    # try:
    # Decodifica el token
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token has expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid token")