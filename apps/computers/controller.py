from datetime import datetime
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

pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user",
        },
    },
    {"$unset": "user_id"},
]


def all_computers(current_page, page_size, search_term):
    start = (current_page - 1) * page_size
    query = {}

    if search_term:
        search_regex = re.escape(search_term)
        query["$or"] = [
            {"departamento": {"$regex": search_regex, "$options": "i"}},
            {"codigo": {"$regex": search_regex, "$options": "i"}},
            {"serie": {"$regex": search_regex, "$options": "i"}},
            {"marca": {"$regex": search_regex, "$options": "i"}},
            {"modelo": {"$regex": search_regex, "$options": "i"}},
            {"user.nombre": {"$regex": search_regex, "$options": "i"}},
        ]

    pipeline_extended = pipeline + [
        {"$match": query},
        {"$skip": start},
        {"$limit": page_size},
    ]

    all_computers_cursor = list(
        connection[DB_NAME].computers.aggregate(pipeline_extended)
    )
    total_records = connection[DB_NAME].computers.count_documents(
        query
    )  # Obtiene el total de registros

    all_computers_serialized = convert_object_ids_to_strings(all_computers_cursor)
    return {
        "data": all_computers_serialized,
        "total_records": total_records,  # Agrega el total de registros al resultado
        "current_page": current_page,
        "page_size": page_size,
    }


def all_computers_export(rangue_date_one, range_date_two):
    date_filter = {"created_at": {"$gte": rangue_date_one, "$lte": range_date_two}}
    all_computers = list(connection[DB_NAME].computers.find(date_filter))

    if len(all_computers) > 0:
        df = pd.DataFrame(convert_object_ids_to_strings(all_computers))

        # Crear un archivo Excel temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            df.to_excel(temp, index=False)

        # Enviar el archivo Excel al cliente
        return FileResponse(
            temp.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="computers.xlsx",
        )
    return JSONResponse(
        status_code=204,
        content={"message": "No hay registros disponibles para exportar"},
    )



def all_computers_name_and_id():
    all_computers = list(
        connection[DB_NAME].computers.find(
            {"deleted": {"$ne": True}},
            projection={
                "departamento": False,
                "serie": False,
                "capacidad_disco": False,
                "memoria_ram": False,
                "soporte_max_ram": False,
                "tarjetas": False,
                "slots": False,
                "slots_dispositivos": False,
                "slots_ocupados": False,
                "user_id": False,
                "fecha_asignacion_usuario": False,
                "description": False,
                "estado": False,
                "office_version": False,
                "year_lanzamiento": False,
                "generacion": False,
                "tipo_perfil": False,
                "ghz_procesador": False,
                "marca_procesador": False,
                "generacion_procesador": False,
                "created_at": False,
                "updated_at": False,
                "deleted_at": False,
                "deleted": False,
            },
        )
    )
    return convert_object_ids_to_strings(all_computers)


def find_one_computers(id: str | int):
    computer = connection[DB_NAME].computers.find_one({"_id": ObjectId(id)})
    if not computer:
        return {"message": "Computer not found"}

    return convert_object_ids_to_strings(computer)


def create_computers(computers):
    new_computers = preprocess_data_create(dict(computers))

    if new_computers["user_id"]:
        new_computers["user_id"] = ObjectId(new_computers["user_id"])
    
    try:
        id = connection[DB_NAME].computers.insert_one(new_computers).inserted_id
        created_computers = connection[DB_NAME].computers.find_one({"_id": id})
        return convert_object_ids_to_strings(created_computers)
    except Exception as error:
        print(error, "error")
        raise HTTPException(
            status_code=401,
            detail=f"{error}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update_computers(id: int, computers):
    new_computers = preprocess_data_update(dict(computers))

    if new_computers["user_id"]:
        new_computers["user_id"] = ObjectId(new_computers["user_id"])
        
    connection[DB_NAME].computers.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": new_computers}
    )

    return convert_object_ids_to_strings(
        connection[DB_NAME].computers.find_one({"_id": ObjectId(id)})
    )


def destroy_computers(id: int):
    element = connection[DB_NAME].computers.find_one_and_update(
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


def reactive_computer(id: int):
    element = connection[DB_NAME].computers.find_one_and_update(
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
