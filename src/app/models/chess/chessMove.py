from app.models.chess.chessPosition import ChessPosition
from app.models.chess.chessPiece import PieceType
from typing import Optional

class ChessMove:
    def __init__(self, fromPos: ChessPosition, toPos: ChessPosition, promotion: Optional[PieceType] = None):
        self.fromPos = fromPos
        self.toPos = toPos
        self.promotion = promotion
