class TicTacToePosition:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if isinstance(other, TicTacToePosition):
            return self.row == other.row and self.col == other.col
        return False
    
    def __hash__(self):
        return hash((self.row, self.col))