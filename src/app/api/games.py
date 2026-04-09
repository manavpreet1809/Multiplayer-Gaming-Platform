"""
Game API router.

Endpoints:
  POST /games/create          - create a new lobby
  GET  /games                 - list waiting public lobbies
  GET  /games/{game_id}       - get game/lobby state
  POST /games/{game_id}/join  - join by game_id
  POST /games/join/code       - join by 4-letter lobby code
  POST /games/matchmake       - join an open lobby or create one
  POST /games/{game_id}/start - start game (host only)
  POST /games/{game_id}/leave - leave game/lobby
  WS   /games/ws/{game_id}   - WebSocket for real-time game updates + lobby chat
  WS   /games/chat/global    - WebSocket for global chat
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.db.ConnectionManager import manager
from app.models.Game import Game
from app.models.GameSettings import GameSettings
from app.models.GameStatus import GameStatus
from app.models.Visibility import Visibility
from app.services.authServices import get_current_user, get_current_user_from_token

router = APIRouter(prefix="/games", tags=["games"])

# ─── In-memory store ──────────────────────────────────────────────────
# Maps game_id -> Game. Both dicts are in-memory (dev-only).
_games: dict[str, Game] = {}
_lobby_codes: dict[str, str] = {}  # lobby_code -> game_id
_global_chat: list[dict] = []      # last N global chat messages (capped at 200)
_global_ws: dict[str, WebSocket] = {}  # username -> websocket for global chat

# ─── Request schemas ──────────────────────────────────────────────────

class CreateGameRequest(BaseModel):
    game_type: str       # "chess" | "tictactoe"
    visibility: str = "public"

class JoinByCodeRequest(BaseModel):
    lobby_code: str

class MatchmakeRequest(BaseModel):
    game_type: str

# ─── Serialization helpers ────────────────────────────────────────────

def _vis_val(v) -> int:
    return v.value if isinstance(v, Visibility) else v

def _status_val(s) -> int:
    return s.value if isinstance(s, GameStatus) else s

def _game_summary(game: Game) -> dict:
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

def _full_response(game: Game) -> dict:
    base = _game_summary(game)
    if game.state:
        base["state"] = game.state.to_dict()
    return base

# ─── REST endpoints ───────────────────────────────────────────────────

@router.post("/create")
async def create_game(body: CreateGameRequest, current_user=Depends(get_current_user)):
    if body.game_type not in ("chess", "tictactoe"):
        raise HTTPException(status_code=400, detail="game_type must be 'chess' or 'tictactoe'")
    vis = Visibility.PUBLIC if body.visibility == "public" else Visibility.PRIVATE
    game = Game(
        game_type=body.game_type,
        host_id=current_user.username,
        visibility=vis,
        settings=GameSettings(2, {}),
    )
    game.addPlayer(current_user.username)
    _games[game.game_id] = game
    _lobby_codes[game.lobby_code] = game.game_id
    return _game_summary(game)


@router.get("")
async def list_games(
    current_user=Depends(get_current_user),
    game_type: Optional[str] = Query(None),
):
    results = []
    for g in _games.values():
        if g.status != GameStatus.WAITING:
            continue
        if g.visibility == Visibility.PRIVATE and g.host_id != current_user.username:
            continue
        if game_type and g.game_type != game_type:
            continue
        results.append(_game_summary(g))
    return results


@router.post("/join/code")
async def join_by_code(body: JoinByCodeRequest, current_user=Depends(get_current_user)):
    game_id = _lobby_codes.get(body.lobby_code.upper())
    if not game_id:
        raise HTTPException(status_code=404, detail="Lobby not found")
    game = _games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.status != GameStatus.WAITING:
        raise HTTPException(status_code=409, detail="Game already started")
    if len(game.player_ids) >= game.settings.max_players:
        raise HTTPException(status_code=409, detail="Lobby is full")
    if current_user.username not in game.player_ids:
        game.addPlayer(current_user.username)
        await manager.broadcast(game_id, {
            "type": "player_joined",
            "player_id": current_user.username,
            "players": game.player_ids,
        })
    return _game_summary(game)


@router.post("/matchmake")
async def matchmake(body: MatchmakeRequest, current_user=Depends(get_current_user)):
    if body.game_type not in ("chess", "tictactoe"):
        raise HTTPException(status_code=400, detail="Invalid game type")
    # Find an open public lobby
    for g in _games.values():
        if (
            g.status == GameStatus.WAITING
            and g.game_type == body.game_type
            and g.visibility == Visibility.PUBLIC
            and len(g.player_ids) < g.settings.max_players
            and current_user.username not in g.player_ids
        ):
            g.addPlayer(current_user.username)
            await manager.broadcast(g.game_id, {
                "type": "player_joined",
                "player_id": current_user.username,
                "players": g.player_ids,
            })
            return _game_summary(g)
    # None found — create a new lobby
    game = Game(
        game_type=body.game_type,
        host_id=current_user.username,
        visibility=Visibility.PUBLIC,
        settings=GameSettings(2, {}),
    )
    game.addPlayer(current_user.username)
    _games[game.game_id] = game
    _lobby_codes[game.lobby_code] = game.game_id
    return _game_summary(game)


@router.get("/{game_id}")
async def get_game(game_id: str, current_user=Depends(get_current_user)):
    game = _games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return _full_response(game)


@router.post("/{game_id}/join")
async def join_game(game_id: str, current_user=Depends(get_current_user)):
    game = _games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.status != GameStatus.WAITING:
        raise HTTPException(status_code=409, detail="Game already started")
    if len(game.player_ids) >= game.settings.max_players:
        raise HTTPException(status_code=409, detail="Lobby is full")
    if current_user.username not in game.player_ids:
        game.addPlayer(current_user.username)
        await manager.broadcast(game_id, {
            "type": "player_joined",
            "player_id": current_user.username,
            "players": game.player_ids,
        })
    return _game_summary(game)


@router.post("/{game_id}/start")
async def start_game(game_id: str, current_user=Depends(get_current_user)):
    game = _games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.host_id != current_user.username:
        raise HTTPException(status_code=403, detail="Only the host can start the game")
    if game.status != GameStatus.WAITING:
        raise HTTPException(status_code=409, detail="Game not in waiting state")
    if len(game.player_ids) < game.settings.max_players:
        raise HTTPException(status_code=409, detail="Not enough players to start")
    game.startGame()
    serialized = game._get_engine().serializeState(game._engine_state)
    await manager.broadcast(game_id, {"type": "game_started", "state": serialized})
    return _full_response(game)


@router.post("/{game_id}/leave")
async def leave_game(game_id: str, current_user=Depends(get_current_user)):
    game = _games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    was_in_progress = game.status == GameStatus.IN_PROGRESS
    game.removePlayer(current_user.username)
    if was_in_progress:
        game.status = GameStatus.FINISHED
        await manager.broadcast(game_id, {
            "type": "game_over",
            "result": {"isOver": True, "result": "forfeit", "winner": None},
            "reason": f"{current_user.username} left the game",
        })
    elif game.player_ids:
        if game.host_id == current_user.username:
            game.host_id = game.player_ids[0]
        await manager.broadcast(game_id, {
            "type": "player_left",
            "player_id": current_user.username,
            "players": game.player_ids,
            "host_id": game.host_id,
        })
    else:
        _games.pop(game_id, None)
        _lobby_codes.pop(game.lobby_code, None)
    return {"success": True}


# ─── WebSocket: per-game room ─────────────────────────────────────────

@router.websocket("/ws/{game_id}")
async def game_websocket(game_id: str, ws: WebSocket):
    token = ws.query_params.get('token')
    if not token:
        await ws.accept()
        await ws.close(code=4001)
        return

    try:
        current_user = await get_current_user_from_token(token)
        print(current_user.username, "connected to game", game_id)
    except Exception:
        await ws.accept()
        await ws.close(code=4001)
        return

    game = _games.get(game_id)
    if not game:
        await ws.accept()
        await ws.close(code=4004)
        return

    await manager.connect(game_id, current_user.username, ws)

    # Send initial state
    try:
        if game.status == GameStatus.IN_PROGRESS and game._engine_state is not None:
            serialized = game._get_engine().serializeState(game._engine_state)
            await ws.send_json({"type": "state", "state": serialized})
        else:
            await ws.send_json({"type": "lobby", "data": _game_summary(game)})
    except Exception:
        pass

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
                await manager.broadcast(game_id, msg)

            elif msg_type == "select_piece":
                if game.status != GameStatus.IN_PROGRESS:
                    continue
                if game.active_player_id != current_user.username:
                    continue
                pos = data.get("position", {})
                fe_row = pos.get("row")
                fe_col = pos.get("col")
                if fe_row is None or fe_col is None:
                    continue
                engine = game._get_engine()
                be_row = 7 - fe_row
                moves = engine.getLegalMovesForSquare(game._engine_state, be_row, fe_col)
                await ws.send_json({"type": "legal_moves", "moves": moves})

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
        if game_id in _games:
            await manager.broadcast(game_id, {
                "type": "player_disconnected",
                "player_id": current_user.username,
            })


# ─── WebSocket: global chat ───────────────────────────────────────────

@router.websocket("/chat/global")
async def global_chat_ws(ws: WebSocket):
    token = ws.query_params.get('token')
    if not token:
        await ws.accept()
        await ws.close(code=4001)
        return

    try:
        current_user = await get_current_user_from_token(token)
    except Exception:
        await ws.accept()
        await ws.close(code=4001)
        return

    await ws.accept()
    _global_ws[current_user.username] = ws

    try:
        await ws.send_json({"type": "history", "messages": _global_chat[-50:]})
    except Exception:
        pass

    try:
        while True:
            data = await ws.receive_json()
            if data.get("type") == "chat":
                text = str(data.get("text", "")).strip()[:500]
                if text:
                    msg = {"type": "chat", "sender": current_user.username, "text": text}
                    _global_chat.append(msg)
                    if len(_global_chat) > 200:
                        del _global_chat[0]
                    dead = []
                    for username, conn in list(_global_ws.items()):
                        try:
                            await conn.send_json(msg)
                        except Exception:
                            dead.append(username)
                    for u in dead:
                        _global_ws.pop(u, None)
    except WebSocketDisconnect:
        _global_ws.pop(current_user.username, None)
