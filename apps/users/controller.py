from datetime import datetime
from config.db_config_nosql import connection
from config.config import DB_NAME
from fastapi import HTTPException
from bson import ObjectId
import re

from utils.date_status import preprocess_data_create, preprocess_data_update
from utils.convert_object_ids_to_strings import convert_object_ids_to_strings

def all_users(current_page, page_size, search_term):
    start = (current_page - 1) * page_size
    query = {}

    if search_term:
        search_regex = re.escape(search_term)
        query["$or"] = [
            {"nombre": {"$regex": search_regex, "$options": "i"}},
            {"apellido": {"$regex": search_regex, "$options": "i"}}
        ]

    all_users = list(connection[DB_NAME].users.find(query).skip(start).limit(page_size))
    all_users_serialized = convert_object_ids_to_strings(all_users)
    return {
        "data": all_users_serialized,
        "current_page": current_page,
        "page_size": page_size,
    }

def all_users_name_and_id():
    all_users = list(connection[DB_NAME].users.find(
        
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
