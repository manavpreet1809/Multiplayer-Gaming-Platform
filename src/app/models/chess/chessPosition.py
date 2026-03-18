class chessPosition:
    def __init__(self, row: int, col: int):
        if not (0 <= row <= 7 and 0 <= col <= 7):
            #TODO decide what error to throw here once we have a proper error handling system
            pass
        self.row = row
        self.col = col