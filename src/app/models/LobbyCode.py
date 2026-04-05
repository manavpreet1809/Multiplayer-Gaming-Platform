from src.app.db.GamesRepository import GamesRepository
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
            # Generate code
            code = "".join(random.choice(LobbyCode.allowedChars) for i in range(LobbyCode.length))

            # Check if it is in use
            is_safe = await GameRepository.isSafeCode(code)
            if is_safe:
                return code