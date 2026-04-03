from mongo import db
import random
import string

game_collection = db["games"]

class LobbyCode:
    allowedChars = string.ascii_letters

    # Generates a lobby code given a length
    @staticmethod
    async def generate_code(length):
        while True:
            code = "".join(random.choice(LobbyCode.allowedChars) for i in range(length))
            is_safe = await LobbyCode.is_safe_code(code)
            if is_safe return code

    # Checks if the code is safe
    @staticmethod
    async def is_safe_code(code):
        conflict = await games_collection.find_one({ "code": code }, { "code": 1 })
        return conflict is None;
