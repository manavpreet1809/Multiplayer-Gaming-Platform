"""
Game API: REST lobbies/matchmaking and WebSocket play/chat.

Run the API with a single Uvicorn worker; see ``store`` module docstring and README.
"""

from fastapi import APIRouter

from app.api.games.routes_rest import register_rest_routes
from app.api.games.routes_ws import register_ws_routes

router = APIRouter(prefix="/games", tags=["games"])
register_rest_routes(router)
register_ws_routes(router)

__all__ = ["router"]
