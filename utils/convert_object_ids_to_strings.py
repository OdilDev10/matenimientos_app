from datetime import datetime
from bson import ObjectId

# TODO: cuando es lista de str no funciona
def convert_object_ids_to_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, (dict, list)):
                convert_object_ids_to_strings(value)
    elif isinstance(data, list):
        for item in data:
            convert_object_ids_to_strings(item)
    return data


def convert_object_ids_list_to_strings(object_ids):
    return [str(object_id) for object_id in object_ids]
