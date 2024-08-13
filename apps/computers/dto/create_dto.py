from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union
from enum import Enum


class Estado(str, Enum):
    DISPONIBLE = "disponible"
    OPERATIVO = "operativo"


class Marca(str, Enum):
    DELL = "dell"
    HP = "hp"
    MSI = "msi"


class Tipo_perfil(str, Enum):
    OFICINA_PRINCIPAL = "oficina principal"
    OFICINA_1000 = "1000 x 1000"


class Marca_procesador(str, Enum):
    INTEL = "intel"
    AMD = "amd"


class CreateComputerDTO(BaseModel):
    # departamento: str
    # codigo: str
    serie: Union[str, None] = None
    capacidad_disco: Union[str, None] = None
    memoria_ram: Union[str, None] = None
    soporte_max_ram: Union[str, None] = None
    tarjetas: Union[int, None] = None
    slots: Union[int, None] = None
    slots_dispositivos: Union[int, None] = None
    slots_ocupados: Union[int, None] = None
    user_id: Union[str, int, None] = None
    fecha_asignacion_usuario: Union[str, None] = None
    description: Union[str, None] = None
    estado: Estado = Field(Estado.DISPONIBLE, description="Computer status")
    marca: Marca = Field(..., description="Marca del equipo")
    modelo: Union[str, None] = None
    office_version: Union[str, None] = None
    year_lanzamiento: Union[str, None] = None
    generacion: Union[str, None] = None
    # tipo_perfil: Tipo_perfil = Field(..., description="Oficina usuario")
    ghz_procesador: Union[str, None] = None
    marca_procesador: Marca_procesador = Field(..., description="Marca procesador")
    generacion_procesador: Union[str, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "departamento": "TI",
                "codigo": "PC-001",
                "serie": "SN123456",
                "capacidad_disco": "1TB",
                "memoria_ram": "16GB",
                "soporte_max_ram": "32GB",
                "tarjetas": 1,
                "slots": 4,
                "slots_dispositivos": 2,
                "slots_ocupados": 2,
                "user_id": "123",
                "fecha_asignacion_usuario": "2023-01-01",
                "description": "Computadora de oficina",
                "estado": "operativo",
                "marca": "dell",
                "modelo": "OptiPlex 7070",
                "office_version": "2019",
                "year_lanzamiento": "2020",
                "generacion": "10th Gen",
                "tipo_perfil": "oficina principal",
                "ghz_procesador": "3.6GHz",
                "marca_procesador": "intel",
                "generacion_procesador": "10th Gen",
            }
        }
