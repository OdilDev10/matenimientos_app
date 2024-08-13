from datetime import datetime
from typing import Optional
from apps.dtos.pagination_dto import GetComputersDTO
from .models import Roles, users_Model
from .dto.create_user import (
    UserCreate,
    UserInDB,
    create_jwt_token,
    hash_password,
    verify_password,
)
from config.db_config_nosql import connection
from config.config import DB_NAME
from fastapi import HTTPException
from bson import ObjectId
import re
from utils.date_status import preprocess_data_create, preprocess_data_update
from utils.convert_object_ids_to_strings import convert_object_ids_to_strings
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import tempfile
from utils.generic_controller import get_all

# # AUTH


def create_users_register(users):
    user = preprocess_data_create(dict(users))
    try:
        # Verificar si el usuario ya existe
        existing_user = connection[DB_NAME].users.find_one({"email": user["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user["password"])
        user["password"] = hashed_password
        connection[DB_NAME].users.insert_one(user)
        return {"msg": "User registered successfully"}
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def users_login(email: str, password: str):
    try:
        existing_user = connection[DB_NAME].users.find_one({"email": email})
        if not existing_user:
            raise HTTPException(status_code=400, detail="Usuario no existe")

        if not verify_password(password, existing_user["password"]):
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")

        token = create_jwt_token(email)
        return {
            "message": "User login successfully",
            "token": token,
            "user": convert_object_ids_to_strings(existing_user),
        }
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# CRUD


def all_clients(
    pagination: GetComputersDTO,
):
    pipeline = [{"$match": {"role": "client"}}]

    return get_all(
        pagination=pagination,
        collection_name="users",
        search_fields=[
            "codigo",
            "serie",
            "marca",
            "modelo",
            "user.nombre",
        ],
        pipeline=pipeline,
    )


def all_users(
    pagination: GetComputersDTO,
):
    pipeline = [{"$match": {"role": "admin"}}]

    return get_all(
        pagination=pagination,
        collection_name="users",
        search_fields=[
            "codigo",
            "serie",
            "marca",
            "modelo",
            "user.nombre",
        ],
        pipeline=pipeline,
    )


def all_users_export(rangue_date_one, range_date_two):
    date_filter = {"created_at": {"$gte": rangue_date_one, "$lte": range_date_two}}
    all_users = list(connection[DB_NAME].users.find(date_filter))

    if len(all_users) > 0:
        df = pd.DataFrame(convert_object_ids_to_strings(all_users))

        # Crear un archivo Excel temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            df.to_excel(temp, index=False)

        # Enviar el archivo Excel al cliente
        return FileResponse(
            temp.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="userss.xlsx",
        )
    return JSONResponse(
        status_code=204,
        content={"message": "No hay registros disponibles para exportar"},
    )


def all_users_name_and_id():
    all_users = list(
        connection[DB_NAME].users.find(
            {"role": "admin", "deleted": {"$ne": True}},
            projection={
                "created_at": False,
                "updated_at": False,
                "deleted_at": False,
                "id": False,
                "deleted": False,
            },
        )
    )
    return convert_object_ids_to_strings(all_users)


def all_users_client_name_and_id():
    all_users = list(
        connection[DB_NAME].users.find(
            {"role": "client", "deleted": {"$ne": True}},
            projection={
                "created_at": False,
                "updated_at": False,
                "deleted_at": False,
                "id": False,
                "deleted": False,
            },
        )
    )
    return convert_object_ids_to_strings(all_users)


def find_one_users(id: str | int):
    user = connection[DB_NAME].users.find_one({"_id": ObjectId(id)})
    if not user:
        return {"message": "user not found"}

    return convert_object_ids_to_strings(user)


def create_users(users):
    new_users = preprocess_data_create(dict(users))

    try:
        id = connection[DB_NAME].users.insert_one(new_users).inserted_id
        created_users = connection[DB_NAME].users.find_one({"_id": id})
        return convert_object_ids_to_strings(created_users)
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update_users(id: int, users):
    new_users = preprocess_data_update(dict(users))

    connection[DB_NAME].users.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": new_users}
    )

    return convert_object_ids_to_strings(
        connection[DB_NAME].users.find_one({"_id": ObjectId(id)})
    )


def destroy_users(id: int):
    element = connection[DB_NAME].users.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "updated_at": datetime.now(),
                "deleted_at": datetime.now(),
                "deleted": True,
            },
        },
        return_document=False,
    )
    return convert_object_ids_to_strings(element)


def reactive_user(id: int):
    element = connection[DB_NAME].users.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "updated_at": datetime.now(),
                "deleted": False,
            },
        },
        return_document=False,
    )

    return convert_object_ids_to_strings(element)
