from datetime import datetime
from config.db_config_nosql import connection
from config.config import DB_NAME
from fastapi import HTTPException
from bson import ObjectId
import re
from utils.date_status import preprocess_data_create, preprocess_data_update
from utils.globalserializer import gobal_serializer
from utils.convert_object_ids_to_strings import convert_object_ids_to_strings
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import tempfile

pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user",
        },
    },
    {
        "$lookup": {
            "from": "computers",
            "localField": "computer_id",
            "foreignField": "_id",
            "as": "computer",
        },
    },
    {"$unset": "user_id"},
    {"$unset": "computer_id"},
]


def all_mantenimiento(current_page, page_size, search_term):
    start = (current_page - 1) * page_size
    query = {}

    if search_term:
        search_regex = re.escape(search_term)
        query["$or"] = [
            {"descripcion_mantenimiento": {"$regex": search_regex, "$options": "i"}},
            {"user.nombre": {"$regex": search_regex, "$options": "i"}},
            {"computer.codigo": {"$regex": search_regex, "$options": "i"}},
        ]

    pipeline_extended = pipeline + [
        {"$match": query},
        {"$skip": start},
        {"$limit": page_size},
    ]

    all_mantenimiento = list(
        connection[DB_NAME].mantenimiento.aggregate(pipeline_extended)
    )

    return {
        "data": convert_object_ids_to_strings(all_mantenimiento),
        "current_page": current_page,
        "page_size": page_size,
    }


def all_mantenimiento_export(rangue_date_one, range_date_two):
    date_filter = {"created_at": {"$gte": rangue_date_one, "$lte": range_date_two}}
    all_mantenimiento = list(connection[DB_NAME].mantenimiento.find(date_filter))

    if len(all_mantenimiento) > 0:
        df = pd.DataFrame(convert_object_ids_to_strings(all_mantenimiento))

        # Crear un archivo Excel temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            df.to_excel(temp, index=False)

        # Enviar el archivo Excel al cliente
        return FileResponse(
            temp.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="mantenimientos.xlsx",
        )
    return JSONResponse(
        status_code=204,
        content={"message": "No hay registros disponibles para exportar"},
    )


def find_one_mantenimiento(id: str | int):
    mantenimiento = connection[DB_NAME].mantenimiento.find_one({"_id": ObjectId(id)})

    if not mantenimiento:
        return {"message": "antenimiento not found"}

    mantenimiento["computer"] = connection[DB_NAME].computers.find_one(
        {"_id": ObjectId(mantenimiento["computer_id"])}
    )
    mantenimiento["user"] = connection[DB_NAME].users.find_one(
        {"_id": ObjectId(mantenimiento["user_id"])}
    )
    del mantenimiento["computer_id"]
    del mantenimiento["user_id"]

    return convert_object_ids_to_strings(mantenimiento)


def create_mantenimiento(mantenimiento):
    new_mantenimiento = preprocess_data_create(dict(mantenimiento))

    new_mantenimiento["computer_id"] = ObjectId(new_mantenimiento["computer_id"])
    new_mantenimiento["user_id"] = ObjectId(new_mantenimiento["user_id"])

    try:
        id = connection[DB_NAME].mantenimiento.insert_one(new_mantenimiento).inserted_id
        created_mantenimiento = connection[DB_NAME].mantenimiento.find_one({"_id": id})
        return convert_object_ids_to_strings(created_mantenimiento)
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update_mantenimiento(id: int, mantenimiento):
    new_mantenimiento = preprocess_data_update(dict(mantenimiento))

    new_mantenimiento["user_id"] = ObjectId(new_mantenimiento["user_id"])
    new_mantenimiento["computer_id"] = ObjectId(new_mantenimiento["computer_id"])

    connection[DB_NAME].mantenimiento.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": new_mantenimiento}
    )

    return convert_object_ids_to_strings(
        connection[DB_NAME].mantenimiento.find_one({"_id": ObjectId(id)})
    )


def destroy_mantenimiento(id: int):
    element = connection[DB_NAME].mantenimiento.find_one_and_update(
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


def reactive_mantenimiento(id: int):
    element = connection[DB_NAME].mantenimiento.find_one_and_update(
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
