from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Union


class ProductImage(BaseModel):
    url: str
    alt_text: str


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


class computers_Model(BaseModel):
    id: Union[str, int, None] = None
    # departamento: str
    # codigo: str
    serie: str
    capacidad_disco: str
    memoria_ram: str
    soporte_max_ram: Union[str, int, None] = None
    tarjetas: Union[str, int, None] = None
    slots: Union[str, int, None] = None
    slots_dispositivos: Union[str, int, None] = None
    slots_ocupados: int
    client_id: Union[str, int, int, None] = None
    user_id: Union[str, int, int, None] = None

    fecha_asignacion_usuario: str
    description: str
    estado: Estado = Field(..., description="Computer status")
    marca: str
    modelo: str
    office_version: Union[str, int, None] = None
    year_lanzamiento: Union[str, int, None] = None
    generacion: Union[str, int, None] = None
    # tipo_perfil: Tipo_perfil = Field(..., description="Oficina usuario")
    ghz_procesador: str
    marca_procesador: Marca_procesador = Field(..., description="Marca procesador")
    generacion_procesador: str
    created_at: datetime = Field(None, description="Product creation date")
    updated_at: datetime = Field(None, description="Last updated timestamp")
    deleted_at: datetime = Field(None, description="Product deletion timestamp")
    deleted: bool = Field(False, description="Whether the Product is marked as deleted")

    class Config:
        populate_by_name = True

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "name": "Producto XYZ",
    #             "images": [{"url": "https://example.com/image1.jpg", "alt_text": "Imagen 1"}, {"url": "https://example.com/image2.jpg", "alt_text": "Imagen 2"}],
    #             "category_id": 1,
    #             "supplier_id": 1,
    #             "price_sale": 100.0,
    #             "price_cost": 80.0,
    #             "description": "Descripción del producto XYZ",
    #             "technology": "Tecnología A"
    #         }
    #     }
