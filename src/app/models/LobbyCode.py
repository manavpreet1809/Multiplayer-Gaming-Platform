from mongo import db
import random
import string

game_collection = db["games"]

class LobbyCode:
    # Parameters
    allowedChars = string.ascii_letters
    length = 4

    # Generates a lobby code given a length
    @staticmethod
    async def generate():
        while True:
            code = "".join(random.choice(LobbyCode.allowedChars) for i in range(LobbyCode.length))
            is_safe = await LobbyCode.is_safe(code)
            if is_safe return code

    # Checks if the code is safe
    @staticmethod
    async def is_safe(code):
        conflict = await games_collection.find_one({ "code": code }, { "code": 1 })
        return conflict is None;
