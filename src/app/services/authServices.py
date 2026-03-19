from src.app.db.validUser import users_collection
from src.app.schemas.user import UserCredentials

def userExists(credentials: UserCredentials) -> bool:
    user = users_collection.find_one({
        "username": credentials.username,
        "password": credentials.password
    })
    return user is not None
