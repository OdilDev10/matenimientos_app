
from datetime import datetime


def preprocess_data_create(data):
    data["created_at"] = datetime.now()
    data["updated_at"] = datetime.now()
    data["deleted_at"] = None
    data["deleted"] = False

    return data


def preprocess_data_update(data):
    del data["created_at"]
    del data["deleted_at"]
    data["updated_at"] = datetime.now()
    del data["deleted"]

    return data