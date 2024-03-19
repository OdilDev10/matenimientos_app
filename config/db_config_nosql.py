from pymongo import MongoClient
from config.config import MONGO_URI

try:
    connection = MongoClient(MONGO_URI)
    print("---Connecting to MONGODB:", connection)
  
except Exception as error:
    print("---Error connecting to MONGODB: ", error)
