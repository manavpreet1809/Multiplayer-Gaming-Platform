from typing import Optional, Any  # mainly for
from gameEngine import GameEngine # type hints

class ValidationPipeline:
    def __init__(self, engine: GameEngine): # pass ChessEngine or TicTacToeEngine
        self.engine = engine

    def processMove(self, state: dict, playerId: str, move: Any) -> dict:
        # check the turn (considers both game engines)
        if "activeColor" in state:
            active_player = state["players"][state["activeColor"]] # for ChessEngine
        else:
            active_player = state["currentPlayer"] # for TicTacToeEngine

        if active_player != playerId:
            return {
                "success": False,
                "error": "not your turn",
                "state": None,
                "result": None
            }
        
        # validate the move
        if not self.engine.validateMove(state, move):
            return {
                "success": False,
                "error": "illegal move",
                "state": None,
                "result": None
            }
        
        # apply the move
        new_state = self.engine.applyMove(state, move)

        # evaluate if the game reached an end state
        result: Optional[dict] = self.engine.evaluateEnd(new_state)

        return {
            "success": True,
            "error": None,
            "state": new_state,
            "result": result
        }