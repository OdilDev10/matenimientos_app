from apps.dtos.pagination_dto import GetComputersDTO
from config.db_config_nosql import connection
from config.config import DB_NAME
from bson import ObjectId
from utils.date_status import preprocess_data_create, preprocess_data_update
from utils.convert_object_ids_to_strings import convert_object_ids_to_strings
from utils.generic_controller import (
    all_data_export,
    create_one_record,
    disable_record,
    find_one_register,
    get_all,
    reactive_register,
    update_one_record,
)

pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "client_id",
            "foreignField": "_id",
            "as": "client",
        },
    },
       {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user",
        },
    },
    {"$unset": "client_id"},
]


def all_computers(
    pagination: GetComputersDTO,
):
    return get_all(
        pagination=pagination,
        collection_name="computers",
        search_fields=[
            "codigo",
            "serie",
            "marca",
            "modelo",
            "user.nombre",
        ],
        pipeline=pipeline,
    )


def all_computers_export(rangue_date_one, range_date_two):
    print('LLEGO')
    return all_data_export(
        collection_name="computers",
        rangue_date_one=rangue_date_one,
        range_date_two=range_date_two,
    )


def all_computers_name_and_id():
    all_computers = list(
        connection[DB_NAME].computers.find(
            {"deleted": {"$ne": True}},
            projection={
                "_id": True,
                "codigo": True,
                "marca": True,
                "modelo": True,
            },
        )
    )
    return convert_object_ids_to_strings(all_computers)


def find_one_computers(id: str | int):
    return find_one_register(collection_name="computers", id=id)


def create_computers(computers):
    new_computers = preprocess_data_create(dict(computers))

    if new_computers["client_id"]:
        new_computers["client_id"] = ObjectId(new_computers["client_id"])

    return create_one_record(collection_name="computers", data=new_computers)


def update_computers(id: int, computers):
    new_computers = preprocess_data_update(dict(computers))

    if new_computers["client_id"]:
        new_computers["client_id"] = ObjectId(new_computers["client_id"])
    return update_one_record("computers", new_computers, id)


def destroy_computers(id: int):
    disable_record("computers", id=id)


def reactive_computer(id: int):
    reactive_register("computers", id=id)
