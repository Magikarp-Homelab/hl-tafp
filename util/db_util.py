import pymongo

from CONSTANTS import MONGO_DB_URL
from CONSTANTS import MONGO_DB_NAME


def get_db_connection():
    client = pymongo.MongoClient(MONGO_DB_URL)
    return client[MONGO_DB_NAME]


def get_collection(col_name):
    db = get_db_connection()
    return db[col_name]
