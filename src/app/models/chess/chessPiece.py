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
    def __init__(self, pieceType: PieceType, color: Color, hasMoved: bool = False):
        self.pieceType = pieceType
        self.color = color
        self.hasMoved = hasMoved