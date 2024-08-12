from datetime import datetime
from dtos.pagination_dto import GetComputersDTO
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

# def all_users(current_page, page_size, search_term):
    # start = (current_page - 1) * page_size
    # query = {}

    # if search_term:
    #     search_regex = re.escape(search_term)
    #     query["$or"] = [
    #         {"nombre": {"$regex": search_regex, "$options": "i"}},
    #         {"apellido": {"$regex": search_regex, "$options": "i"}}
    #     ]

    # all_users = list(connection[DB_NAME].users.find(query).skip(start).limit(page_size))
    # all_users_serialized = convert_object_ids_to_strings(all_users)
    # return {
    #     "data": all_users_serialized,
    #     "current_page": current_page,
    #     "page_size": page_size,
    # }

pipeline = [
  
    {"$unset": "client_id"},
]

def all_users(
    pagination: GetComputersDTO,
):
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
    all_users = list(connection[DB_NAME].users.find(
        {"deleted": {"$ne": True}},
         projection={
                "created_at": False,
                "updated_at": False,
                "deleted_at": False,
                "id": False,
                "deleted": False
            },
    ))
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
