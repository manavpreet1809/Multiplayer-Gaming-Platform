from typing import Optional, Any
from app.modules.gameEngine import GameEngine


class ValidationPipeline:
    def __init__(self, engine: GameEngine):
        self.engine = engine

    def processMove(self, state: dict, playerId: str, move: Any) -> dict:
        if "activeColor" in state:
            active_player = state["players"][state["activeColor"]]
        else:
            active_player = state["currentPlayer"]

        if active_player != playerId:
            return {
                "success": False,
                "error": "not your turn",
                "state": None,
                "result": None
            }

        if not self.engine.validateMove(state, move):
            return {
                "success": False,
                "error": "illegal move",
                "state": None,
                "result": None
            }

        new_state = self.engine.applyMove(state, move)

        raw_result: Optional[dict] = self.engine.evaluateEnd(new_state)
        result = self.engine.serializeEndResult(raw_result, new_state) if raw_result else None

        return {
            "success": True,
            "error": None,
            "state": new_state,
            "result": result
        }