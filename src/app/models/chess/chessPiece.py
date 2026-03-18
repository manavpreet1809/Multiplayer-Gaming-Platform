from enum import Enum

class PieceType(Enum):
    KING = "KING"
    QUEEN = "QUEEN"
    ROOK = "ROOK"
    BISHOP = "BISHOP"
    KNIGHT = "KNIGHT"
    PAWN = "PAWN"


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class ChessPiece:
    def __init__(self, piece_type: PieceType, color: Color, has_moved: bool = False):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = has_moved