from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from GamesRepository import GameRepository
from db.ConnectionManager import manager
from datetime import datetime

app = FastAPI()

@app.websocket("/ws/game/{game_id}")
async def game_websocket(websocket: WebSocket, game_id: str, player_id: str):
    await manager.connect(game_id, player_id, websocket)
    
    try:
        # Every connection to the game; useful for broadcasting updates to other sockets besides the current
        players = manager.active_connections[game_id]

        while True:
            data = await websocket.receive_json()
            event = data.get("event")
            payload = data.get("payload")

            game = await GameRepository.getGame(game_id)
            if not game:
                await websocket.send_json({"event": "error", "message": "Game not found"})
                continue

            if event == "make_move":
                if player_id not in game.player_ids:
                    await websocket.send_json({"event": "move_rejected", "reason": "Not a participant"})
                    continue
                
                if str(game.state.current_player) != player_id:
                    await websocket.send_json({"event": "move_rejected", "reason": "Not your turn"})
                    continue

                if game.isValid(payload):
                    game.move(payload)
                    
                    move_entry = {"player_id": player_id, "action": "make_move", "payload": payload, "timestamp": datetime.uctnow().isoformat()}
                    await GameRepository.updateGameState(game_id, game.state.to_dict(), move_entry)

                    await manager.broadcast(game_id, {"event": "game_state_update", "payload": game.toDict(), "timestamp": datetime.uctnow().isoformat()})
                else:
                    await websocket.send_json({"event": "move_rejected", "reason": "Invalid move"})

            if event == "leave":
                # If the player is a spectator, reject
                if player_id not in game.player_ids:
                    await websocket.send_json({ "event": "leave_rejected", "reason": "Not a participant" })
                    continue

                # If the player is the host, transfer it to someone else first
                if player_id == game.host_id and len(game.player_ids) > 1:
                    # We swap to the first player that isn't the host
                    # Two cases: either the current host is at index 0, or they aren't
                    new_host = game.player_ids[1 if game.player_ids[0] == game.host_id else 0]
                    await GameRepository.changeHost(game_id, new_host)

                    # Broadcast a message to update to the new host
                    for ws in players:
                        await ws.send_json({ "event": "host_change", "payload": { "id": new_host } })
                
                # Kick the player
                await GameRepository.removePlayer(game_id, player_id)
                
                # Broadcast a message to update players in front-end
                for ws in players:
                    await ws.send_json({ "event": "player_left", "payload": { "id": player_id } })

                # Terminate the WebSocket
                await websocket.close(code = 1000, reason = "Player initiated leave request")

                # TODO: Forfeit the game if it is running

                # If that was the last player, shut down the entire lobby
                if len(game.player_ids) == 1:
                    pass # TODO: Shut down lobby
                
            if event == "kick":
                target = payload.target_id

                # If the player is not the host, reject
                if player_id != game.host_id:
                    await websocket.send_json({ "event": "kick_rejected", "reason": "Not the host" })
                    continue

                # If the target is not in-game, reject
                if target not in game.player_ids:
                    await websocket.send_json({ "event": "kick_rejected", "reason": "Player not in game" })
                    continue

                # Otherwise, kick the player
                await GameRepository.removePlayer(game_id, target)

                # Host-only message, notifying them of their successful kick
                await websocket.send_json({ "event": "kick_success", "message": "Kicked player successfully" })

                # Message to update the player list in the front-end
                for ws in players:
                    await ws.send_json({ "event": "player_kicked", "payload": { "id": target_id } })

                # Terminate the WebSocket for the kicked player
                await players[target_id].send_json({ "event": "kicked", "message": "Player kicked" })
                await players[target_id].close(code = 1000, reason = "Player kicked")


    except WebSocketDisconnect:
        manager.disconnect(game_id, player_id)

        await manager.broadcast(game_id, {
            "event": "player_disconnected",
            "player_id": player_id
        })
