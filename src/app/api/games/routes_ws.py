import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.ConnectionManager import manager
from app.models.GameStatus import GameStatus
from app.services.authServices import get_current_user_from_token

from app.api.games import store

logger = logging.getLogger(__name__)


async def _resolve_ws_token(ws: WebSocket) -> str | None:
    """
    Token may be passed as a query param (legacy) or as the first JSON message:
    ``{"type": "auth", "token": "<jwt>"}``. Prefer the message form so tokens are
    less likely to appear in HTTP access logs.
    """
    token = ws.query_params.get("token")
    if token:
        return token
    try:
        data = await ws.receive_json()
    except Exception as exc:
        logger.debug("WebSocket first frame failed: %s", exc)
        return None
    if isinstance(data, dict) and data.get("type") == "auth" and data.get("token"):
        return data["token"]
    return None


def register_ws_routes(router: APIRouter) -> None:
    @router.websocket("/ws/{game_id}")
    async def game_websocket(game_id: str, ws: WebSocket):
        await ws.accept()

        token = await _resolve_ws_token(ws)
        if not token:
            await ws.close(code=4001)
            return

        try:
            current_user = await get_current_user_from_token(token)
        except Exception as exc:
            logger.debug("WebSocket game auth failed: %s", exc, exc_info=True)
            await ws.close(code=4001)
            return

        game = store.get_game(game_id)
        if not game:
            await ws.close(code=4004)
            return

        if current_user.username not in game.player_ids:
            await ws.close(code=4003)
            return

        await manager.connect(game_id, current_user.username, ws, already_accepted=True)
        logger.debug("User %s connected to game %s", current_user.username, game_id)

        try:
            if game.status == GameStatus.IN_PROGRESS and game._engine_state is not None:
                serialized = game._get_engine().serializeState(game._engine_state)
                await ws.send_json({"type": "state", "state": serialized})
            else:
                await ws.send_json({"type": "lobby", "data": store.game_summary(game)})
        except Exception as exc:
            logger.debug("WebSocket initial state send failed: %s", exc)

        try:
            while True:
                data = await ws.receive_json()
                msg_type = data.get("type")

                if msg_type == "move":
                    if game.status != GameStatus.IN_PROGRESS:
                        await ws.send_json({"type": "error", "error": "Game not in progress"})
                        continue
                    if game.active_player_id != current_user.username:
                        await ws.send_json({"type": "error", "error": "Not your turn"})
                        continue
                    engine = game._get_engine()
                    try:
                        move_obj = engine.deserializeMove(data["move"], game._engine_state)
                    except Exception as e:
                        await ws.send_json({"type": "error", "error": f"Invalid move format: {e}"})
                        continue
                    outcome = game.move(move_obj)
                    if not outcome["success"]:
                        await ws.send_json({"type": "error", "error": outcome["error"]})
                        continue
                    serialized = engine.serializeState(game._engine_state)
                    msg = {"type": "state", "state": serialized}
                    if outcome["result"]:
                        msg["result"] = outcome["result"]
                    if outcome.get("status"):
                        msg["status"] = outcome["status"]
                    if outcome["result"] and outcome["result"].get("isOver"):
                        await store.record_game_result(game, serialized, outcome["result"])
                    await manager.broadcast(game_id, msg)

                elif msg_type == "chat":
                    text = str(data.get("text", "")).strip()[:500]
                    if text:
                        await manager.broadcast(game_id, {
                            "type": "chat",
                            "sender": current_user.username,
                            "text": text,
                        })

        except WebSocketDisconnect:
            manager.disconnect(game_id, current_user.username)
            if store.get_game(game_id):
                await manager.broadcast(game_id, {
                    "type": "player_disconnected",
                    "player_id": current_user.username,
                })

    @router.websocket("/chat/global")
    async def global_chat_ws(ws: WebSocket):
        await ws.accept()

        token = await _resolve_ws_token(ws)
        if not token:
            await ws.close(code=4001)
            return

        try:
            current_user = await get_current_user_from_token(token)
        except Exception as exc:
            logger.debug("WebSocket global chat auth failed: %s", exc, exc_info=True)
            await ws.close(code=4001)
            return

        registry = store.global_ws_registry()
        registry[current_user.username] = ws

        try:
            await ws.send_json({"type": "history", "messages": store.global_chat_messages()[-50:]})
        except Exception as exc:
            logger.debug("WebSocket global history send failed: %s", exc)

        try:
            while True:
                data = await ws.receive_json()
                if data.get("type") == "chat":
                    text = str(data.get("text", "")).strip()[:500]
                    if text:
                        msg = {"type": "chat", "sender": current_user.username, "text": text}
                        store.global_chat_messages().append(msg)
                        gc = store.global_chat_messages()
                        if len(gc) > 200:
                            del gc[0]
                        dead = []
                        for username, conn in list(registry.items()):
                            try:
                                await conn.send_json(msg)
                            except Exception:
                                dead.append(username)
                        for u in dead:
                            registry.pop(u, None)
        except WebSocketDisconnect:
            registry.pop(current_user.username, None)
