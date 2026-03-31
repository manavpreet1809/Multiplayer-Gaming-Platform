class GameState:
    def __init__(self):
        self.board = [[], [], []] #TODO have a method that initializes an empty board
        self.data = {} #TODO e.g. in chess, tracking what pieces were taken
        self.current_player = 123 #TODO current player whose turn it is

    def toDict(self):
        return {
            "board": self.board,
            "data": self.data,
            "current_player": self.current_player
        }
    
    @staticmethod
    def fromDict(data):
        if not data: return GameState()
        return GameState(data.get("board"), data.get("data"), data.get("current_player"))