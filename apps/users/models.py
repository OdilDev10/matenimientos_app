from datetime import datetime
from enum import Enum
from enum import Enum
from pydantic import BaseModel, Field
from typing import Union


class Roles(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"



class Role(str, Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"


classC(BaseModel):
    id: Union[str, int, None] = None
    name: str
    last_name: str
    age: int
    email: str = Field(None, description="User email address")
    password: str
    role: Roles = Field(default=Roles.CLIENT, description="User role", )
    created_at: datetime = Field(None, description="Mantenimiento creation date")
    updated_at: datetime = Field(None, description="Last updated timestamp")
    deleted_at: datetime = Field(None, description="Mantenimiento deletion timestamp")
    deleted: bool = Field(
        False, description="Whether the Mantenimiento is marked as deleted"
    )

    class Config:
        populate_by_name = True
