from typing import List, Union
from fastapi import APIRouter, Depends, Query, HTTPException
from .controller import (
    all_users,
    all_users_name_and_id,
    create_users,
    destroy_users,
    find_one_users,
    reactive_user,
    update_users,
)
from .models import users_Model

router_users = APIRouter()


@router_users.get(
    "/users",
    tags=["users".upper()],
)
def get_users(
    current_page: int = Query(1, description="Número de página", ge=1),
    page_size: int = Query(10, description="Resultados por página", le=1000),
    search_term: str = Query("", description="Término de búsqueda"),
):
    try:
        return all_users(current_page, page_size, search_term)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_users.get(
    "/users_name_id",
    tags=["users".upper()],
)
def get_users():
    try:
        return all_users_name_and_id()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_users.post("/users", tags=["users".upper()])
def post_users(
    users: users_Model,
):
    try:
        return create_users(users)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_users.get("/users/{id}", tags=["users".upper()])
def get_users(
    id: str,
):
    try:
        return find_one_users(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_users.put("/users/{id}", tags=["users".upper()])
def put_users(
    id: str,
    users: users_Model,
):
    try:

        return update_users(id, users)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )



@router_users.put("/users_active/{id}", tags=["users".upper()])
def put_users_reactive(
    id: str,
):
    try:

        return reactive_user(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router_users.delete("/users/{id}", tags=["users".upper()])
def delete_users(
    id: str,
):
    try:
        return destroy_users(id)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
