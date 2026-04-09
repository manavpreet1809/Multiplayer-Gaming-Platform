class GameState:
    def __init__(self, board=None, data=None, current_player=None):
        self.board = board
        self.data = data if data is not None else {}
        self.current_player = current_player

    def to_dict(self) -> dict:
        return {
            "board": self.board,
            "data": self.data,
            "current_player": self.current_player,
        }

    @staticmethod
    def from_dict(data: dict) -> "GameState":
        if not data:
            return GameState()
        return GameState(
            board=data.get("board"),
            data=data.get("data"),
            current_player=data.get("current_player"),
        )
