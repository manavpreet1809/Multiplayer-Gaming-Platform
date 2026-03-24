from typing import Optional, List
from chessPosition import chessPosition
from chessPiece import ChessPiece, PieceType, Color


class chessBoard:
    def __init__(self):
        # 8x8 grid initialized to None
        self.grid: List[List[Optional[ChessPiece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def setupInitialPosition(self):
        # Pawns
        for col in range(8):
            self.grid[1][col] = ChessPiece(PieceType.PAWN, Color.WHITE)
            self.grid[6][col] = ChessPiece(PieceType.PAWN, Color.BLACK)

        # Rooks
        self.grid[0][0] = ChessPiece(PieceType.ROOK, Color.WHITE)
        self.grid[0][7] = ChessPiece(PieceType.ROOK, Color.WHITE)
        self.grid[7][0] = ChessPiece(PieceType.ROOK, Color.BLACK)
        self.grid[7][7] = ChessPiece(PieceType.ROOK, Color.BLACK)

        # Knights
        self.grid[0][1] = ChessPiece(PieceType.KNIGHT, Color.WHITE)
        self.grid[0][6] = ChessPiece(PieceType.KNIGHT, Color.WHITE)
        self.grid[7][1] = ChessPiece(PieceType.KNIGHT, Color.BLACK)
        self.grid[7][6] = ChessPiece(PieceType.KNIGHT, Color.BLACK)

        # Bishops
        self.grid[0][2] = ChessPiece(PieceType.BISHOP, Color.WHITE)
        self.grid[0][5] = ChessPiece(PieceType.BISHOP, Color.WHITE)
        self.grid[7][2] = ChessPiece(PieceType.BISHOP, Color.BLACK)
        self.grid[7][5] = ChessPiece(PieceType.BISHOP, Color.BLACK)

        # Queens
        self.grid[0][3] = ChessPiece(PieceType.QUEEN, Color.WHITE)
        self.grid[7][3] = ChessPiece(PieceType.QUEEN, Color.BLACK)

        # Kings
        self.grid[0][4] = ChessPiece(PieceType.KING, Color.WHITE)
        self.grid[7][4] = ChessPiece(PieceType.KING, Color.BLACK)

    def getPiece(self, position: chessPosition) -> Optional[ChessPiece]:
        return self.grid[position.row][position.col]

    def setPiece(self, position: chessPosition, piece: ChessPiece):
        self.grid[position.row][position.col] = piece

    def removePiece(self, position: chessPosition):
        self.grid[position.row][position.col] = None

    def toList(self) -> list:
        """Serialize to an 8x8 list of piece codes (or None) for the frontend.

        The frontend expects row 0 = rank 8 (black's back rank), but the
        backend stores row 0 = rank 1 (white's back rank).  This method
        reverses the row order so the output matches the frontend convention.
        """
        result = []
        for r in reversed(range(8)):          # row 7 → 0 in backend = row 0 → 7 for frontend
            row = []
            for c in range(8):
                piece = self.grid[r][c]
                row.append(piece.toCode() if piece is not None else None)
            result.append(row)
        return result