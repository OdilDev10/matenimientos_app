from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from apps.users.models import Roles

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(email: str):
    expiration = datetime.now() + timedelta(hours=1)  # Token expira en 1 hora
    token = jwt.encode(
        {"sub": email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM
    )
    return token