from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from GamesRepository import GameRepository
from db.ConnectionManager import manager
from datetime import datetime

app = FastAPI()

@app.websocket("/ws/game/{game_id}")
async def game_websocket(websocket: WebSocket, game_id: str, player_id: str):
    await manager.connect(game_id, player_id, websocket)
    
    try:
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
                    
                    move_entry = {"player_id": player_id, "action": "make_move", "payload": payload, "timestamp": datetime.utcnow().isoformat()}
                    await GameRepository.updateGameState(game_id, game.state.to_dict(), move_entry)

                    await manager.broadcast(game_id, {"event": "game_state_update", "payload": game.to_dict(), "timestamp": datetime.utcnow().isoformat()})
                else:
                    await websocket.send_json({"event": "move_rejected", "reason": "Invalid move"})

    except WebSocketDisconnect:
        manager.disconnect(game_id, player_id)

        await manager.broadcast(game_id, {
            "event": "player_disconnected",
            "player_id": player_id
        })