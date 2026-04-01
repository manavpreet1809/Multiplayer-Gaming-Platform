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

# =====

import random

# Yes I typed these out by hand
# I know, I know, don't thank me
allowedChars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

# Generates a lobby code given a length
def generateCode(length):
    # The intention of the while-true loop here is to make you wait long enough to ruminate
    # upon your life as a programmer. What caused you to take such a horrible and
    # masochistic career path full of pain and Linux?
    # Ok maybe Linux is a good thing
    # But like what else, who in their right mind wants to type gcc main.c over and over?
    # Is that even the right command? Have my classes failed me?
    # Wait a minute this is Python
    # Yeah
    # I still hate it
    # Here in python we have pip blah blah blah
    # The villain takes on many names
    # And you know what the worst part is?
    # Lemon
    while True:
        code = "".join(random.choice(allowedChars) for i in range(length))
        if isSafeCode(code) return code

# Checks if a given join code is in use
# This is probably validation team's job but too late
# My muscle memory overrides the needs of the validation team
# But if they wish they can remove this and then write their own thing instead
# Who knows, maybe they don't like me querying the database a lot for this
# Oh well
def isSafeCode(code):
    return lobbies.find_one({ "code": code }, { "code": 1 }) is None;

# =====

# Create lobby
@app.post("/lobbies")
def createLobby(user, visibility, maxPlayers):
    # TODO: Validation checks
    query = users.find_one({ "_id": user }, { "currentLobby": 1 })

    if query.currentLobby is None:
        # Generate 4-letter code
        code = generateCode(4)

        # Create a lobby with the user as host
        lobby = {}
        lobby.code = code
        lobby.visibility = visibility
        lobby.maxPlayers = maxPlayers
        lobby.players = [user]
        lobby.host = user
        lobby.status = 0 # now where did that enum go when i need it TODO

        # Insert the lobby into the database
        lobbies.insert_one(lobby)

        lobbyId = 1 # exception remover v1.0 ok but seriously how do we get the lobby id, TODO
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