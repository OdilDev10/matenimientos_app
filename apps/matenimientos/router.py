from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Request

from apps.dtos.pagination_dto import GetComputersDTO
from apps.users.dto.create_user import create_jwt_token, decode_jwt_token

# from apps.auth.controller import get_user_disabled_current
# from apps.users.schemas import SchemaEntityusers
from .controller import (
    all_mantenimiento,
    all_mantenimiento_export,
    create_mantenimiento,
    destroy_mantenimiento,
    find_maintenance_by_client_id,
    find_one_mantenimiento,
    reactive_mantenimiento,
    update_mantenimiento,
)
from .models import mantenimiento_Model

router_mantenimiento = APIRouter()


@router_mantenimiento.get(
    "/mantenimiento",
    tags=["mantenimiento".upper()],
)
def get_mantenimiento(
    # request: Request,
    idUser: str = Query("", description="Id cliente"),
    current_page: int = Query(1, description="Número de página", ge=1),
    page_size: int = Query(10, description="Resultados por página", le=1000),
    search_term: str = Query("", description="Término de búsqueda"),
    # user: SchemaEntityusers = Depends(get_user_disabled_current),
):

    try:
        return all_mantenimiento(current_page, page_size, search_term, idUser)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.get(
    "/mantenimiento_by_client",
    tags=["mantenimiento".upper()],
)
def get_mantenimiento(
    # request: Request,
    idUser: str = Query("", description="Id cliente"),
    params: GetComputersDTO = Depends(),
):

    try:
        return find_maintenance_by_client_id(params, idUser)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.get(
    "/mantenimiento/export/{range_date_one}/{range_date_two}",
    tags=["mantenimiento".upper()],
)
def get_mantenimiento_to_export(
    range_date_one: datetime,
    range_date_two: datetime,
    # user: SchemaEntityusers = Depends(get_user_disabled_current),
):
    try:
        return all_mantenimiento_export(range_date_one, range_date_two)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.post("/mantenimiento", tags=["mantenimiento".upper()])
def post_mantenimiento(
    mantenimiento: mantenimiento_Model,
):
    try:
        return create_mantenimiento(mantenimiento)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.get("/mantenimiento/{id}", tags=["mantenimiento".upper()])
def get_mantenimiento(
    id: str,
):
    try:
        return find_one_mantenimiento(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.put("/mantenimiento/{id}", tags=["mantenimiento".upper()])
def put_mantenimiento(
    id: str,
    mantenimiento: mantenimiento_Model,
):
    try:

        return update_mantenimiento(id, mantenimiento)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.put("/mantenimiento_active/{id}", tags=["mantenimiento".upper()])
def put_mantenimiento_reactive(
    id: str,
):
    try:

        return reactive_mantenimiento(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_mantenimiento.delete("/mantenimiento/{id}", tags=["mantenimiento".upper()])
def delete_mantenimiento(
    id: str,
):
    try:
        return destroy_mantenimiento(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
