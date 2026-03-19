#use this to check if user exist from the db
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["myapp"]
users_collection = db["users"]


#schemas