import os

from numpy.ma.extras import unique
from pymongo import AsyncMongoClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongo://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "myapp")

client = AsyncMongoClient(MONGODB_URL)
db = client[DB_NAME]
users_collection = db["users"]

async def create_indexes():
    await users_collection.create_indexes("username", unique=True)


def close_mongo_connection():
    client.close()