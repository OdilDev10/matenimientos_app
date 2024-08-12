from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Union


class Role(str, Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"


classC(BaseModel):
    id: Union[str, int, None] = None
    nombre: str
    role: Role = Field(Role.CLIENTE, description="Marca procesador")
    apellido: str
    created_at: datetime = Field(None, description="Mantenimiento creation date")
    updated_at: datetime = Field(None, description="Last updated timestamp")
    deleted_at: datetime = Field(None, description="Mantenimiento deletion timestamp")
    deleted: bool = Field(
        False, description="Whether the Mantenimiento is marked as deleted"
    )

    class Config:
        populate_by_name = True
