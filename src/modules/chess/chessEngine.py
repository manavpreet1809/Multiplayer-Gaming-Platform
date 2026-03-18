from typing import List, Optional
from modules.gameEngine import GameEngine

class ChessEngine(GameEngine):
    def createInitialState(self, players: List[str]) -> dict:
        return True

    def validateMove(self, state: dict, move: dict) -> bool:
        return True

    def applyMove(self, state: dict, move: dict) -> dict:
        return state

    def evaluateEnd(self, state: dict) -> Optional[dict]:
        return None