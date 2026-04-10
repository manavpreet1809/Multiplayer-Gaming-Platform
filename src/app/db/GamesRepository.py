# Handles all db operations for the games collection

from mongo import db
from datetime import datetime
from models.Game import Game
from models.GameState import GameState

games_collection = db["games"]

class GameRepository:

    # Creates a new game
    @staticmethod
    async def createGame(game: Game):
        doc = game.to_dict()
        doc["createdAt"] = datetime.utcnow()
        await games_collection.insert_one(doc)
        return game.game_id

    # Creates a game from the db
    @staticmethod
    async def getGame(game_id: str):
        doc = await games_collection.find_one({"_id": game_id})
        if not doc:
            return None
        
        game = Game(game_id=doc["_id"], lobby_code=doc["lobby_code"], visibility=doc["visibility"], status=doc["status"], host_id=doc["host_id"])
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