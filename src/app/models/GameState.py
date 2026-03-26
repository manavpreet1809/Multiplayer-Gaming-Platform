class GameState:
    def __init__(self):
        self.board = [[], [], []] #TODO have a method that initializes an empty board
        self.data = {} #TODO e.g. in chess, tracking what pieces were taken
        self.current_player = 123 #TODO current player whose turn it is