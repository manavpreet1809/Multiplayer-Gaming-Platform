from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(
        self,
        id: str,
        player_id: str,
        websocket: WebSocket,
        *,
        already_accepted: bool = False,
    ):
        if not already_accepted:
            await websocket.accept()
        if id not in self.active_connections:
            self.active_connections[id] = {}
        self.active_connections[id][player_id] = websocket

    def disconnect(self, id: str, player_id: str):
        if id in self.active_connections:
            self.active_connections[id].pop(player_id, None)
            if not self.active_connections[id]:
                del self.active_connections[id]

    async def broadcast(self, id: str, message: dict):
        if id in self.active_connections:
            for connection in self.active_connections[id].values():
                await connection.send_json(message)

manager = ConnectionManager()