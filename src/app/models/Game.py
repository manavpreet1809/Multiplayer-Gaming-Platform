import uuid
import random
import string
from typing import Optional, List

from app.models.Visibility import Visibility
from app.models.GameStatus import GameStatus
from app.models.GameSettings import GameSettings
from app.models.GameState import GameState

_SUPPORTED_GAME_TYPES = {"chess", "tictactoe"}


def _make_engine(game_type: str):
    if game_type == "chess":
        from app.modules.chess.chessEngine import ChessEngine
        return ChessEngine()
    if game_type == "tictactoe":
        from app.modules.TicTacToe.TicTacToeEngine import TicTacToeEngine
        return TicTacToeEngine()
    raise ValueError(f"Unsupported game type: {game_type!r}")


def _generate_lobby_code(length: int = 4) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Game:
    def __init__(
        self,
        game_type: str,
        host_id: str,
        visibility: Visibility = Visibility.PUBLIC,
        settings: Optional[GameSettings] = None,
        game_id: Optional[str] = None,
        lobby_code: Optional[str] = None,
        status: GameStatus = GameStatus.WAITING,
    ):
        if game_type not in _SUPPORTED_GAME_TYPES:
            raise ValueError(f"Unsupported game type: {game_type!r}")
        self.game_id: str = game_id or str(uuid.uuid4())
        self.lobby_code: str = lobby_code or _generate_lobby_code()
        self.game_type: str = game_type
        self.visibility: Visibility = visibility
        self.status: GameStatus = status
        self.host_id: str = host_id
        self.player_ids: List[str] = []
        self.active_player_id: Optional[str] = None
        self.settings: GameSettings = settings or GameSettings(2, {})
        self.state: Optional[GameState] = None
        self.move_history: list = []
        self._engine = None
        self._engine_state = None

    # ------------------------------------------------------------------ engine

    def _get_engine(self):
        if self._engine is None:
            self._engine = _make_engine(self.game_type)
        return self._engine

    # ------------------------------------------------------------------ lifecycle

    def startGame(self):
        """Transition WAITING -> IN_PROGRESS and initialise board state via the engine."""
        engine = self._get_engine()
        self._engine_state = engine.createInitialState(self.player_ids)
        self.state = GameState.from_dict(engine.serializeState(self._engine_state))
        self.active_player_id = self.player_ids[0] if self.player_ids else None
        self.status = GameStatus.IN_PROGRESS

    # ------------------------------------------------------------------ player management

    def addPlayer(self, player_id: str):
        if player_id not in self.player_ids:
            self.player_ids.append(player_id)

    def removePlayer(self, player_id: str):
        try:
            self.player_ids.remove(player_id)
            if self.active_player_id == player_id:
                self.active_player_id = self.player_ids[0] if self.player_ids else None
        except ValueError:
            pass

    # ------------------------------------------------------------------ game logic

    def isValid(self, move) -> bool:
        if self._engine_state is None:
            return False
        return self._get_engine().validateMove(self._engine_state, move)

    def move(self, move) -> dict:
        """Validate and apply a move. Returns a pipeline result dict."""
        from app.modules.validationPipeline import ValidationPipeline
        if self._engine_state is None:
            return {"success": False, "error": "game not started", "state": None, "result": None}
        engine = self._get_engine()
        pipeline = ValidationPipeline(engine)
        outcome = pipeline.processMove(self._engine_state, self.active_player_id, move)
        if outcome["success"]:
            self._engine_state = outcome["state"]
            serialized = engine.serializeState(self._engine_state)
            self.state = GameState.from_dict(serialized)
            self.move_history.append(serialized)
            self.nextTurn()
            if outcome["result"] and outcome["result"].get("isOver"):
                self.status = GameStatus.FINISHED
        return outcome

    def nextTurn(self):
        """Advance active_player_id to whoever the engine says moves next."""
        if self._engine_state is None or not self.player_ids:
            return
        raw = self._engine_state
        if "activeColor" in raw:
            self.active_player_id = raw["players"][raw["activeColor"]]
        elif "currentPlayer" in raw:
            self.active_player_id = raw["currentPlayer"]

    # ------------------------------------------------------------------ serialization

    def to_dict(self) -> dict:
        return {
            "_id": self.game_id,
            "lobby_code": self.lobby_code,
            "game_type": self.game_type,
            "visibility": self.visibility.value if isinstance(self.visibility, Visibility) else self.visibility,
            "status": self.status.value if isinstance(self.status, GameStatus) else self.status,
            "host_id": self.host_id,
            "player_ids": self.player_ids,
            "active_player_id": self.active_player_id,
            "settings": {
                "max_players": self.settings.max_players,
                "rules": self.settings.rules,
            },
            "current_state": self.state.to_dict() if self.state else None,
            "move_history": self.move_history,
        }

    @staticmethod
    def from_dict(data: dict) -> "Game":
        if not data:
            return None
        settings_data = data.get("settings") or {}
        settings = GameSettings(
            settings_data.get("max_players", 2),
            settings_data.get("rules", {}),
        )
        visibility_raw = data.get("visibility", Visibility.PUBLIC.value)
        status_raw = data.get("status", GameStatus.WAITING.value)
        game = Game(
            game_type=data.get("game_type", "chess"),
            host_id=data.get("host_id", ""),
            visibility=Visibility(visibility_raw) if isinstance(visibility_raw, int) else visibility_raw,
            settings=settings,
            game_id=data.get("_id"),
            lobby_code=data.get("lobby_code"),
            status=GameStatus(status_raw) if isinstance(status_raw, int) else status_raw,
        )
        game.player_ids = data.get("player_ids", [])
        game.active_player_id = data.get("active_player_id")
        game.state = GameState.from_dict(data.get("current_state"))
        game.move_history = data.get("move_history", [])
        return game
