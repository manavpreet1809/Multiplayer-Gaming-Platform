from app.models.ConnectionStatus import ConnectionStatus
from app.models.PlayerRole import PlayerRole


class Player:
    def __init__(self, player_id: str, name: str, game_id: str = None, role: PlayerRole = PlayerRole.SPECTATOR):
        self.player_id: str = player_id
        self.name: str = name
        self.game_id: str = game_id
        self.connection_status: ConnectionStatus = ConnectionStatus.DISCONNECTED
        self.role: PlayerRole = role

    def reconnect(self):
        self.connection_status = ConnectionStatus.CONNECTED

    def disconnect(self):
        self.connection_status = ConnectionStatus.DISCONNECTED

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "game_id": self.game_id,
            "connection_status": self.connection_status.value,
            "role": self.role.value,
        }

    @staticmethod
    def from_dict(data: dict) -> "Player":
        player = Player(
            player_id=data["player_id"],
            name=data["name"],
            game_id=data.get("game_id"),
            role=PlayerRole(data.get("role", PlayerRole.SPECTATOR.value)),
        )
        player.connection_status = ConnectionStatus(
            data.get("connection_status", ConnectionStatus.DISCONNECTED.value)
        )
        return player