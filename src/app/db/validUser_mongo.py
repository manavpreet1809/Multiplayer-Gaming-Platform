import os

from pymongo import AsyncMongoClient, IndexModel, ASCENDING

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "myapp")

client = AsyncMongoClient(MONGODB_URL)
db = client[DB_NAME]
users_collection = db["users"]

async def create_indexes():
    # create_indexes() requires a list of IndexModel objects, not a raw string.
    await users_collection.create_indexes([
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("email", ASCENDING)], unique=True, sparse=True),
    ])

def close_mongo_connection():
    client.close()