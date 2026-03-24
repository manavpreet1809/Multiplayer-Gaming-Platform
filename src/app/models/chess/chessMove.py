from app.models.chess.chessPosition import chessPosition
from app.models.chess.chessPiece import PieceType
from typing import Optional

class chessMove:
    def __init__(self, fromPos: chessPosition, toPos: chessPosition, promotion: Optional[PieceType] = None):
        self.fromPos = fromPos
        self.toPos = toPos
        self.promotion = promotion
