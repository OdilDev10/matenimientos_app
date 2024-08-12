from datetime import datetime
import re
import tempfile
from typing import List, Optional

from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
from pydantic import BaseModel
from apps.dtos.pagination_dto import GetComputersDTO
from config.config import DB_NAME
from config.db_config_nosql import connection
from utils import response_error
from utils.convert_object_ids_to_strings import convert_object_ids_to_strings
from utils.date_status import preprocess_data_create


def get_all(
    pagination: GetComputersDTO,
    collection_name: str,
    search_fields: List[str],
    pipeline: Optional[List[dict]] = None,
):
    try:
        current_page = pagination.current_page
        page_size = pagination.page_size
        search_term = pagination.search_term

        start = (current_page - 1) * page_size

        query = {}

        if search_term:
            search_regex = re.escape(search_term)
            query["$or"] = [
                {field: {"$regex": search_regex, "$options": "i"}}
                for field in search_fields
            ]

        if pipeline:
            pipeline_extended = pipeline + [
                {"$match": query},
                {"$skip": start},
                {"$limit": page_size},
            ]

            all_data_cursor = list(
                connection[DB_NAME][collection_name].aggregate(pipeline_extended)
            )
        else:
            all_data_cursor = list(
                connection[DB_NAME][collection_name]
                .find(query)
                .skip(start)
                .limit(page_size)
            )

        total_records = connection[DB_NAME][collection_name].count_documents(query)

        all_data_serialized = convert_object_ids_to_strings(all_data_cursor)
        return {
            "data": all_data_serialized,
            "total_records": total_records,
            "current_page": current_page,
            "page_size": page_size,
        }
    except Exception as error:
        print(f"Error: {error} occurred in GenericController.get_all")
        response_error(error, "get_all in GenericController")


def all_data_export(collection_name: str, rangue_date_one, range_date_two):
    try:
        date_filter = {"created_at": {"$gte": rangue_date_one, "$lte": range_date_two}}
        all_data = list(connection[collection_name].find(date_filter))

        print('LLEGO')

        if len(all_data) > 0:
            df = pd.DataFrame(convert_object_ids_to_strings(all_data))

            # Crear un archivo Excel temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
                df.to_excel(temp.name, index=False)
                temp_path = temp.name

            # Enviar el archivo Excel al cliente
            return FileResponse(
                temp_path,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"{collection_name}.xlsx",
            )

        return JSONResponse(
            status_code=204,
            content={"message": "No hay registros disponibles para exportar"},
        )

    except Exception as error:
        print(f"Error occurred: {error}")
        return  response_error(error, "get_all in GenericController")


def find_one_register(collection_name: str, id: str | int):
    data = connection[DB_NAME][collection_name].find_one({"_id": ObjectId(id)})
    if not data:
        return {"message": "Record not found"}

    return convert_object_ids_to_strings(data)


def create_one_record(collection_name: str, data):
    try:
        id = connection[DB_NAME][collection_name].insert_one(data).inserted_id
        return find_one_register(id=id)
    except Exception as error:
        response_error(error, "Create computer")


def update_one_record(
    collection_name: str,
    data,
    id: int,
):

    connection[DB_NAME][collection_name].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": data}
    )

    return find_one_register(id=id)


def disable_record(collection_name: str, id: int):
    element = connection[DB_NAME][collection_name].find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "updated_at": datetime.now(),
                "deleted_at": datetime.now(),
                "deleted": True,
            },
        },
        return_document=True,
    )
    return convert_object_ids_to_strings(element)


def reactive_register(collection_name: str, id: int):
    element = connection[DB_NAME][collection_name].find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "updated_at": datetime.now(),
                "deleted": False,
            },
        },
        return_document=True,
    )

    return convert_object_ids_to_strings(element)
