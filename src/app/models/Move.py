import uuid
from datetime import datetime, timezone


class MoveRecord:
    """An immutable record of a single move applied in a game."""

    def __init__(self, game_id: str, player_id: str, move_data: dict, timestamp: datetime = None):
        self.move_id: str = str(uuid.uuid4())
        self.game_id: str = game_id
        self.player_id: str = player_id
        self.move_data: dict = move_data
        self.timestamp: datetime = timestamp or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "_id": self.move_id,
            "game_id": self.game_id,
            "player_id": self.player_id,
            "move_data": self.move_data,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "MoveRecord":
        record = MoveRecord(
            game_id=data["game_id"],
            player_id=data["player_id"],
            move_data=data["move_data"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
        )
        record.move_id = data.get("_id", record.move_id)
        return record