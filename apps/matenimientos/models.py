from datetime import datetime
from pydantic import BaseModel, Field
from typing import  Union


class mantenimiento_Model(BaseModel):
    id: Union[str, int, None] = None
    descripcion_mantenimiento: str  = Field(None, description="Mantenimiento descripcion")
    user_id: str
    computer_id: Union[str, int, None] = None
    created_at: datetime = Field(None, description="Mantenimiento creation date")
    updated_at: datetime = Field(None, description="Last updated timestamp")
    deleted_at: datetime = Field(None, description="Mantenimiento deletion timestamp")
    deleted: bool = Field(False, description="Whether the Mantenimiento is marked as deleted")
    
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

