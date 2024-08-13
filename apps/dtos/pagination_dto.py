from fastapi import Query
from pydantic import BaseModel


class GetComputersDTO(BaseModel):
    current_page: int = Query(1, description="Número de página", ge=1)
    page_size: int = Query(10, description="Resultados por página", le=1000)
    search_term: str = Query("", description="Término de búsqueda")
