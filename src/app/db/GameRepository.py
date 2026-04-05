# Handles all DB operations for the games collection

from mongo import db
from datetime import datetime
from models.Game import Game
from models.GameState import GameState

games_collection = db["games"]
users_collection = db["users"]

class GameRepository:

    # Creates a new game
    @staticmethod
    async def createGame(game: Game):
        # Set the game in the DB
        doc = game.to_dict()
        doc["createdAt"] = datetime.utcnow()
        await games_collection.insert_one(doc)

        # Set the current game for the host
        await users.update_one({ "_id": game.host_id }, { "$set": { "current_game": game.game_id } })

        return game.game_id

    # Creates a game from the DB
    @staticmethod
    async def getGame(game_id: str):
        doc = await games_collection.find_one({ "_id": game_id })
        return GameRepository.docToGame(doc)
    
    # Creates a game from the DB using a code
    @staticmethod
    async def getGameByCode(lobby_code: str):
        doc = await games_collection.find_one({ "lobby_code": lobby_code })
        return GameRepository.docToGame(doc)

    # Converts a doc to an instantiated member of the Game class
    @staticmethod
    def docToGame(doc):
        # If nothing was found, return
        if not doc:
            return None
        
        # Instantiate the Game class
        game = Game(
            game_id = doc["_id"],
            lobby_code = doc["lobby_code"],
            visibility = doc["visibility"],
            status = doc["status"],
            host_id = doc["host_id"]
        )

        game.player_ids = doc.get("player_ids", [])
        game.active_player_id = doc.get("active_player_id")
        game.state = GameState.from_dict(doc.get("current_state"))
        game.move_history = doc.get("move_history", [])

        return game

    # Updates the list of players in the current session
    @staticmethod
    async def updatePlayerMembership(game_id: str, player_ids: list):
        await games_collection.update_one({"_id": game_id}, {"$set": {"player_ids": player_ids, "updated_at": datetime.utcnow()}})

    # Updates the game board
    @staticmethod
    async def updateGameState(game_id: str, new_state: dict, move_entry: dict):
        await games_collection.update_one({"_id": game_id}, {"$set": {"current_state": new_state, "updated_at": datetime.utcnow()}, "$push": {"move_history": move_entry}})

    # Adds player to game; used for join functionality
    @staticmethod
    async def addPlayer(game_id: str, player_id: str):
        await games_collection.update_one({ "_id": game_id }, { "$push": { "player_ids": player_id } })
        await users_collection.update_one({ "_id": player_id }, { "$set": { "current_game": game_id } })

    # Removes player from game; used for leave and kick functionality
    @staticmethod
    async def removePlayer(game_id: str, player_id: str):
        await games_collection.update_one({ "_id": game_id }, { "$pull": { "player_ids": player_id } })
        await users_collection.update_one({ "_id": player_id }, { "$set": { "current_game": None } })

    # Swaps host to given player
    @staticmethod
    async def changeHost(game_id: str, player_id: str):
        await games_collection.update_one({ "_id": game_id }, { "$set": { "host_id": player_id } })

    # Deletes a given lobby; used to clean up lobbies if all players leave before the game has started
    @staticmethod
    async def killLobby(game_id: str):
        await games_collection.delete_one({ "_id": game_id })

    # Checks code availability
    @staticmethod
    async def isSafeCode(code: str):
        conflict = await games_collection.find_one({ "code": code })
        return conflict is None;