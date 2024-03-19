from dotenv import load_dotenv
import os
from passlib.context import CryptContext

load_dotenv()
DEBUG = os.getenv("DEBUG")
print("---DEBUG: ", DEBUG)

if DEBUG == "True":
    MONGO_URI = os.getenv("DEV_MONGO_URI")
    DB_NAME = os.getenv("DEV_DB_NAME")
else:
    MONGO_URI = os.getenv("PROD_MONGO_URI")
    DB_NAME = os.getenv("PROD_DB_NAME")

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

valid_roles = ["admin", "client"]