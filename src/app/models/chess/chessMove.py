from chessPosition import chessPosition
from chessPiece import PieceType
from typing import Optional

class chessMove:
    def __init__(self, fromPos: chessPosition, toPos: chessPosition, promotion: Optional[PieceType] = None):
        self.fromPos = fromPos
        self.toPos = toPos
        self.promotion = promotion
