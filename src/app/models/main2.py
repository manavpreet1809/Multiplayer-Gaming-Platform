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
@app.post("/api/lobbies")
def apiCreateLobby(user, visibility, maxPlayers):
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
@app.post("/api/lobbies/join")
def apiJoinLobby(user, lobbyId, lobbyCode):
    # The sheer insanity of writing code blindly without an IDE
    # I got what I wanted but is it really worth it?
    # ...
    # ...anyways this line determines whether we select by id or the lobby code
    if lobbyCode is not None:
        lobby = lobbies.find_one({ "code": lobbyCode }, { "maxPlayers": 1, "players": 1 })
        # Again how do we get the id TODO
    else:
        lobby = lobbies.find_one({ "code": lobbyId }, { "maxPlayers": 1, "players": 1 })

    # Isn't validation... validation team's job?
    # Oh well too bad
    # Client UI did our job last time so this time I'm doing validation's
    # ...what even is a pipeline??? I just learnt this in class today
    # finally fixed my sleep schedule enough to attend
    # just ignore the fact that this is probably committed at like 3 am or something
    if lobby is not None and (len(lobby.players) + 1) <= lobby.maxPlayers and lobby.status is 0:
        lobbies.update_one({ "_id": lobbyId }, { "$push": { "players": user } }) # Add user to lobby
        users.update_one({ "_id": user }, { "$set": { "currentLobby": lobbyId } }) # Update user's status

    # meh it's okay
    # I guess it meets the requirements

# Leave lobby
@app.post("/api/lobbies/leave")
def apiLeaveLobby(user):
    # WAIT WHAT A MAIN MENU STATE???????
    # WHAT WHY I guess it's better BUT WHY
    # why is this the first time I'm hearing of it
    # is it bad that I just heard of it
    # Yeah I guess it's better to have that variable instead of calculating from the currentGame column
    # O(1) vs O(1), but 1 of the O(1) better
    # Speaking of which what does the collections table for users even look like
    # Have I just been writing pure gibberish this whole time, setting columns that don't even exist...
    # .....
    # ...ehhh I think I'll pass on the main menu state for now

    user = users.find_one({ "_id": user }, { "currentLobby": 1 })

    if user.currentLobby is not None:
        lobbies.update_one({ "_id": user.currentLobby }, { "$pull": { "players": user } }) # Remove user from lobby
        lobbies.delete_one({ "_id": user.currentLobby, "host": user }) # Remove lobby if host leaves TODO need to kick other players too 
        users.update_one({ "_id": user }, { "$set": { "currentLobby": None } }) # Update user's status
    
    # Oh crud I forgot the host leaving case
    # Yeah
    # Let's just pretend that's validation team's job and keep quiet
    # ...
    # ...nah it shouldn't be too hard to implement

    # Microsoft would be reeling if they hired me and found all these comments in their codebase
    # ...so would my team... crap

    # Wait a minute what am I doing
    # Shouldn't I make functions for
    # Yes yes I should TODO

# TODO: Leader-only remove user action