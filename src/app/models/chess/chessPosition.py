class chessPosition:
    def __init__(self, row: int, col: int):
        if not (0 <= row <= 7 and 0 <= col <= 7):
            #TODO decide what error to throw here once we have a proper error handling system
            pass
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, chessPosition) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))