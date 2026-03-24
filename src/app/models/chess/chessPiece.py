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
    # Maps PieceType to the single-letter code used by the frontend.
    # Uppercase = white, lowercase = black.
    PIECE_CODE = {
        PieceType.KING:   "K",
        PieceType.QUEEN:  "Q",
        PieceType.ROOK:   "R",
        PieceType.BISHOP: "B",
        PieceType.KNIGHT: "N",
        PieceType.PAWN:   "P",
    }

    def __init__(self, pieceType: PieceType, color: Color, hasMoved: bool = False):
        self.pieceType = pieceType
        self.color = color
        self.hasMoved = hasMoved

    def toCode(self) -> str:
        """Return single-character piece code (uppercase=white, lowercase=black)."""
        code = self.PIECE_CODE[self.pieceType]
        return code if self.color == Color.WHITE else code.lower()