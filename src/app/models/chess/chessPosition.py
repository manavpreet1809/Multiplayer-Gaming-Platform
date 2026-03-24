class chessPosition:
    def __init__(self, row: int, col: int):
        if not (0 <= row <= 7 and 0 <= col <= 7):
            raise ValueError(f"Invalid chess position: row={row}, col={col} (must be 0-7)")
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, chessPosition) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))