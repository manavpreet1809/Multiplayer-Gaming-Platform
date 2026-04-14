"""
In-memory game lobby / match state.

Game documents and WebSocket connections live in this process only. Run Uvicorn with
``--workers 1`` for consistent behaviour; restarting the server clears lobbies and
in-progress games. See README (Run the Project) for details.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import WebSocket
from pydantic import BaseModel

from app.models.Game import Game
from app.models.GameStatus import GameStatus
from app.models.Visibility import Visibility
from app.services.authServices import update_user_stats

logger = logging.getLogger(__name__)

_games: dict[str, Game] = {}
_lobby_codes: dict[str, str] = {}
_global_chat: list[dict] = []
_global_ws: dict[str, WebSocket] = {}


class CreateGameRequest(BaseModel):
    game_type: str
    visibility: str = "public"


class JoinByCodeRequest(BaseModel):
    lobby_code: str


class MatchmakeRequest(BaseModel):
    game_type: str


def _vis_val(v) -> int:
    return v.value if isinstance(v, Visibility) else v


def _status_val(s) -> int:
    return s.value if isinstance(s, GameStatus) else s


def game_summary(game: Game) -> dict:
    return {
        "game_id": game.game_id,
        "lobby_code": game.lobby_code,
        "game_type": game.game_type,
        "visibility": _vis_val(game.visibility),
        "status": _status_val(game.status),
        "host_id": game.host_id,
        "player_ids": game.player_ids,
        "player_count": len(game.player_ids),
        "max_players": game.settings.max_players,
    }


def full_response(game: Game) -> dict:
    base = game_summary(game)
    if game.state:
        base["state"] = game.state.to_dict()
    return base


def normalize_game_type(raw: str) -> str:
    if not raw:
        return "overall"
    normalized = raw.strip().lower().replace("-", "").replace(" ", "")
    return normalized if normalized in {"overall", "chess", "tictactoe"} else "overall"


async def record_game_result(
    game: Game,
    serialized_state: dict,
    result: dict,
    forfeited_user: str | None = None,
):
    if not result or not result.get("isOver"):
        return

    game_type = game.game_type
    players = serialized_state.get("players", {}) if isinstance(serialized_state, dict) else {}

    if result.get("result") == "draw":
        for username in players.values():
            await update_user_stats(username, game_type, "draw")
        return

    if result.get("result") == "win":
        winner_key = result.get("winner")
        winner = players.get(winner_key)
        loser = next((user for key, user in players.items() if user != winner), None)
        if winner:
            await update_user_stats(winner, game_type, "win")
        if loser:
            await update_user_stats(loser, game_type, "loss")
        return

    if result.get("result") == "forfeit":
        if forfeited_user:
            remaining = next((user for user in players.values() if user != forfeited_user), None)
            if remaining:
                await update_user_stats(remaining, game_type, "win")
            await update_user_stats(forfeited_user, game_type, "loss")
        else:
            for username in players.values():
                await update_user_stats(username, game_type, "loss")


def get_game(game_id: str) -> Optional[Game]:
    return _games.get(game_id)


def put_game(game: Game) -> None:
    _games[game.game_id] = game
    _lobby_codes[game.lobby_code] = game.game_id


def remove_game(game: Game) -> None:
    _games.pop(game.game_id, None)
    _lobby_codes.pop(game.lobby_code, None)


def all_games():
    return _games.values()


def lobby_code_to_game_id(code: str) -> Optional[str]:
    return _lobby_codes.get(code.upper())


def global_chat_messages():
    return _global_chat


def global_ws_registry():
    return _global_ws


def reset_runtime_state() -> None:
    """Clear in-memory lobbies (for tests only)."""
    _games.clear()
    _lobby_codes.clear()


__all__ = [
    "CreateGameRequest",
    "JoinByCodeRequest",
    "MatchmakeRequest",
    "logger",
    "game_summary",
    "full_response",
    "normalize_game_type",
    "record_game_result",
    "get_game",
    "put_game",
    "remove_game",
    "all_games",
    "lobby_code_to_game_id",
    "global_chat_messages",
    "global_ws_registry",
    "reset_runtime_state",
]
