from pymongo import MongoClient
from fastapi import FastApi

 # TODO: Don't worry about this, I'll fix it eventually
client = MongoClient("mongodb://localhost:27017/") # TODO: Url

 # TODO: Don't worry about this, I'll fix it eventually
db = client["DATABASE_NAME"] # TODO: DB name, hook up to DB
users = db["users"]
lobbies = db["lobbies"]

# Users (not in the scope of my role, just a dummy variable, also id should be auto-assigned)
# TODO: Don't worry about this, I'll fix it eventually
users.insert_one({ "_id": 1, "username": "test", "displayName": "George", "currentLobby": None })
users.insert_one({ "_id": 2, "username": "test2", "displayName": "Not George", "currentLobby": None })

# Create lobby
@app.post("/lobby/create") # TODO: Don't worry about this, I'll fix it eventually
def createLobby(user, gameType, maxPlayers): # TODO: Don't worry about this, I'll fix it eventually
    lobbyId = 1 # TODO: auto-assign ids
    query = users.find_one({ "_id": user }, { "currentLobby": 1 })

    if query.currentLobby is None:
        lobbies.insert_one({ "_id": lobbyId, "type": gameType, "maxPlayers": maxPlayers, "players": [user], "leader": user }) # Create empty lobby, add user
        users.update_one({ "_id": user }, { "$set": { "currentLobby": lobbyId } }) # Update user's status

# Join lobby
@app.post("/lobby/join") # TODO: Don't worry about this, I'll fix it eventually
def joinLobby(lobby, user): # TODO: Don't worry about this, I'll fix it eventually
    query = lobbies.find_one({ "_id": lobby }, { "maxPlayers": 1, "players": 1 })

    if (len(query.players) + 1) <= query.maxPlayers:
        lobbies.update_one({ "_id": lobby }, { "$push": { "players": user } }) # Add user to lobby
        users.update_one({ "_id": user }, { "$set": { "currentLobby": lobby } }) # Update user's status

# Leave lobby
@app.post("/lobby/leave") # TODO: Don't worry about this, I'll fix it eventually
def leaveLobby(user): # TODO: Don't worry about this, I'll fix it eventually
    query = users.find_one({ "_id": user }, { "currentLobby": 1 })

    if query.currentLobby is not None:
        lobbies.update_one({ "_id": query.currentLobby }, { "$pull": { "players": user } }) # Remove user from lobby
        users.update_one({ "_id": user }, { "$set": { "currentLobby": None } }) # Update user's status

# TODO: Leader-only remove user action