from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.db.ConnectionManager import manager
from app.models.Game import Game
from app.models.GameSettings import GameSettings
from app.models.GameStatus import GameStatus
from app.models.Visibility import Visibility
from app.db.usersRepo import users_collection
from app.services.authServices import (
    get_current_user,
    limiter,
    normalize_stats,
)

from app.api.games import store


def register_rest_routes(router: APIRouter) -> None:
    @router.post("/create")
    @limiter.limit("30/minute")
    async def create_game(
        request: Request,
        body: store.CreateGameRequest,
        current_user=Depends(get_current_user),
    ):
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
        store.put_game(game)
        return store.game_summary(game)

    @router.get("")
    async def list_games(
        current_user=Depends(get_current_user),
        game_type: Optional[str] = Query(None),
    ):
        results = []
        for g in store.all_games():
            if g.status != GameStatus.WAITING:
                continue
            if g.visibility == Visibility.PRIVATE and g.host_id != current_user.username:
                continue
            if game_type and g.game_type != game_type:
                continue
            results.append(store.game_summary(g))
        return results

    @router.post("/join/code")
    @limiter.limit("60/minute")
    async def join_by_code(
        request: Request,
        body: store.JoinByCodeRequest,
        current_user=Depends(get_current_user),
    ):
        game_id = store.lobby_code_to_game_id(body.lobby_code.upper())
        if not game_id:
            raise HTTPException(status_code=404, detail="Lobby not found")
        game = store.get_game(game_id)
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
        return store.game_summary(game)

    @router.post("/matchmake")
    @limiter.limit("60/minute")
    async def matchmake(
        request: Request,
        body: store.MatchmakeRequest,
        current_user=Depends(get_current_user),
    ):
        if body.game_type not in ("chess", "tictactoe"):
            raise HTTPException(status_code=400, detail="Invalid game type")
        for g in store.all_games():
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
                return store.game_summary(g)
        game = Game(
            game_type=body.game_type,
            host_id=current_user.username,
            visibility=Visibility.PUBLIC,
            settings=GameSettings(2, {}),
        )
        game.addPlayer(current_user.username)
        store.put_game(game)
        return store.game_summary(game)

    @router.get("/leaderboard")
    async def get_leaderboard(
        current_user=Depends(get_current_user),
        game_type: Optional[str] = Query("overall"),
        limit: int = Query(50, ge=1, le=100),
    ):
        normalized = store.normalize_game_type(game_type)
        cursor = users_collection.find(
            {},
            projection={"username": 1, "stats": 1, "_id": 0},
        )
        users = await cursor.to_list(length=500)

        def entry(doc: dict) -> dict:
            stats = normalize_stats(doc.get("stats"))
            if normalized == "overall":
                bucket = stats["overall"]
            else:
                bucket = stats["games"].get(normalized, {})

            tier = bucket.get("rank", "Bronze")
            return {
                # `rank` kept for backward compatibility — value is MMR tier (Bronze/Silver/…), not ordinal.
                "rank": tier,
                "tier": tier,
                "username": doc.get("username", ""),
                "mmr": bucket.get("mmr", 1000),
                "wins": bucket.get("wins", 0),
                "losses": bucket.get("losses", 0),
                "ties": bucket.get("ties", 0),
                "games_played": bucket.get("games_played", 0),
            }

        sorted_rows = sorted(
            (entry(doc) for doc in users),
            key=lambda r: (-r["mmr"], -r["wins"], r["losses"], r["username"]),
        )
        return [{**row, "place": i + 1} for i, row in enumerate(sorted_rows[:limit])]

    @router.get("/{game_id}")
    async def get_game(game_id: str, current_user=Depends(get_current_user)):
        game = store.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        if current_user.username not in game.player_ids:
            raise HTTPException(status_code=403, detail="Not a participant in this game")
        return store.full_response(game)

    @router.post("/{game_id}/join")
    @limiter.limit("60/minute")
    async def join_game(
        request: Request,
        game_id: str,
        current_user=Depends(get_current_user),
    ):
        game = store.get_game(game_id)
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
        return store.game_summary(game)

    @router.post("/{game_id}/start")
    @limiter.limit("20/minute")
    async def start_game(
        request: Request,
        game_id: str,
        current_user=Depends(get_current_user),
    ):
        game = store.get_game(game_id)
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
        return store.full_response(game)

    @router.post("/{game_id}/leave")
    @limiter.limit("60/minute")
    async def leave_game(
        request: Request,
        game_id: str,
        current_user=Depends(get_current_user),
    ):
        game = store.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        was_in_progress = game.status == GameStatus.IN_PROGRESS
        game.removePlayer(current_user.username)
        if was_in_progress:
            game.status = GameStatus.FINISHED
            serialized = game._get_engine().serializeState(game._engine_state) if game._engine_state is not None else {}
            await store.record_game_result(
                game,
                serialized,
                {"isOver": True, "result": "forfeit", "winner": None},
                forfeited_user=current_user.username,
            )
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
            store.remove_game(game)
        return {"success": True}
