from typing import List, Union
from fastapi import APIRouter, Depends, Query, HTTPException

# from apps.auth.controller import get_user_disabled_current
# from apps.users.schemas import SchemaEntityusers
from .controller import (
    all_computers,
    all_computers_name_and_id,
    create_computers,
    destroy_computers,
    find_one_computers,
    reactive_computer,
    update_computers,
)
from .models import computers_Model

router_computers = APIRouter()


@router_computers.get(
    "/computers",
    tags=["computers".upper()],
)
def get_computers(
    current_page: int = Query(1, description="Número de página", ge=1),
    page_size: int = Query(10, description="Resultados por página", le=1000),
    search_term: str = Query("", description="Término de búsqueda"),
    # user: SchemaEntityusers = Depends(get_user_disabled_current),
):
    try:
        return all_computers(current_page, page_size, search_term)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )



@router_computers.get(
    "/computers_name_id",
    tags=["computers".upper()],
)
def get_users_name_and_id():
    try:
        return all_computers_name_and_id()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_computers.post("/computers", tags=["computers".upper()])
def post_computers(
    computers: computers_Model,
):
    try:
        return create_computers(computers)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_computers.get("/computers/{id}", tags=["computers".upper()])
def get_computers(
    id: str,
):
    try:
        return find_one_computers(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_computers.put("/computers/{id}", tags=["computers".upper()])
def put_computers(
    id: str,
    computers: computers_Model,
):
    try:

        return update_computers(id, computers)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_computers.put("/computers_active/{id}", tags=["computers".upper()])
def put_computers_reactive(
    id: str,
):
    try:

        return reactive_computer(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_computers.delete("/computers/{id}", tags=["computers".upper()])
def delete_computers(
    id: str,
):
    try:
        return destroy_computers(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
