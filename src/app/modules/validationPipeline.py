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
            error = "illegal move"

            
            if "activeColor" in state:
                try:
                    active_color = state["activeColor"]
                    opponent = self._opponent_color(active_color)
                    king_pos = self.engine.findKing(state["board"], active_color)
                    in_check = self.engine.isSquareAttacked(state["board"], king_pos, opponent)
                    has_legal = self.engine.hasAnyLegalMove(state, active_color)

                    if in_check and not has_legal:
                        error = "checkmate"
                    elif in_check:
                        error = "check"
                except Exception:
                    pass

            return {
                "success": False,
                "error": error,
                "state": None,
                "result": None
            }

        new_state = self.engine.applyMove(state, move)

        raw_result: Optional[dict] = self.engine.evaluateEnd(new_state)
        result = self.engine.serializeEndResult(raw_result, new_state) if raw_result else None

        status = None
        if "activeColor" in new_state:
            try:
                active_color = new_state["activeColor"]
                opponent = self._opponent_color(active_color)
                king_pos = self.engine.findKing(new_state["board"], active_color)
                in_check = self.engine.isSquareAttacked(new_state["board"], king_pos, opponent)
                if in_check:
                    status = "check"
            except Exception:
                pass

        if result and result.get("isOver") and result.get("reason") == "checkmate":
            status = "checkmate"

        return {
            "success": True,
            "error": None,
            "state": new_state,
            "result": result,
            "status": status,
        }

    @staticmethod
    def _opponent_color(color):
        if hasattr(color, "name"):
            enum_type = type(color)
            return enum_type.BLACK if color.name == "WHITE" else enum_type.WHITE
        return "black" if color == "white" else "white"