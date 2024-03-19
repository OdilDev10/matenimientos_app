from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union

class users_Model(BaseModel):
    id: Union[str, int, None] = None
    nombre: str
    apellido: str
    created_at: datetime = Field(None, description="Mantenimiento creation date")
    updated_at: datetime = Field(None, description="Last updated timestamp")
    deleted_at: datetime = Field(None, description="Mantenimiento deletion timestamp")
    deleted: bool = Field(False, description="Whether the Mantenimiento is marked as deleted")
    
    class Config:
        populate_by_name = True


