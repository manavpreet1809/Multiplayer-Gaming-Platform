from chessPosition import chessPosition
from chessPiece import PieceType
from typing import Optional

class chessMove:
    def __init__(self, from_pos: chessPosition, to_pos: chessPosition, promotion: Optional[PieceType] = None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.promotion = promotion
