from typing import Optional, List
from chessPosition import chessPosition
from chessPiece import ChessPiece, PieceType, Color


class chessBoard:
    def __init__(self):
        # 8x8 grid initialized to None
        self.grid: List[List[Optional[ChessPiece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def setup_initial_position(self):
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

    def get_piece(self, position: chessPosition) -> Optional[ChessPiece]:
        return self.grid[position.row][position.col]

    def set_piece(self, position: chessPosition, piece: ChessPiece):
        self.grid[position.row][position.col] = piece

    def remove_piece(self, position: chessPosition):
        self.grid[position.row][position.col] = None