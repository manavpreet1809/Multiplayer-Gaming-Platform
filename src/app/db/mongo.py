# Connects app to MongoDB

import os
from pymongo import AsyncMongoClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "myapp")

client = AsyncMongoClient(MONGODB_URL)
db = client[DB_NAME]

async def close_mongo_connection():
    client.close()