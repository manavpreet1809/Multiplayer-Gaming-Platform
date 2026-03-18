from typing import List, Optional
from modules.gameEngine import GameEngine
from app.models.chess.chessBoard import chessBoard
from app.models.chess.chessPiece import Color, PieceType, ChessPiece
from app.models.chess.chessMove import chessMove
from app.models.chess.chessPosition import chessPosition

class ChessEngine(GameEngine):
    def createInitialState(self, players: List[str]) -> dict:
        board = chessBoard()
        board.setupInitialPosition()
        return {
            "board": board,
            "players": {
                Color.WHITE: players[0],
                Color.BLACK: players[1],
            },
            "activeColor": Color.WHITE,
            "castlingRights": {
                Color.WHITE: {"kingside": True, "queenside": True},
                Color.BLACK: {"kingside": True, "queenside": True},
            },
            "enPassantTarget": None,
            "halfmoveClock": 0,
        }

    def validateMove(self, state: dict, move: chessMove) -> bool:
        return True

    def applyMove(self, state: dict, move: chessMove) -> dict:
        board = state["board"]
        piece = board.getPiece(move.fromPos)
        captured = board.getPiece(move.toPos)

        # basic move
        board.removePiece(move.fromPos)
        board.setPiece(move.toPos, piece)
        piece.hasMoved = True

        # castling — move the rook
        if piece.pieceType == PieceType.KING and abs(move.toPos.col - move.fromPos.col) == 2:
            if move.toPos.col > move.fromPos.col:
                # kingside: rook goes from col 7 to col 5
                rook = board.getPiece(chessPosition(move.fromPos.row, 7))
                board.removePiece(chessPosition(move.fromPos.row, 7))
                board.setPiece(chessPosition(move.fromPos.row, 5), rook)
                rook.hasMoved = True
            else:
                # queenside: rook goes from col 0 to col 3
                rook = board.getPiece(chessPosition(move.fromPos.row, 0))
                board.removePiece(chessPosition(move.fromPos.row, 0))
                board.setPiece(chessPosition(move.fromPos.row, 3), rook)
                rook.hasMoved = True
            state["castlingRights"][piece.color]["kingside"] = False
            state["castlingRights"][piece.color]["queenside"] = False

        # revoke castling rights on king/rook move
        if piece.pieceType == PieceType.KING:
            state["castlingRights"][piece.color]["kingside"] = False
            state["castlingRights"][piece.color]["queenside"] = False
        elif piece.pieceType == PieceType.ROOK:
            if move.fromPos.col == 7:
                state["castlingRights"][piece.color]["kingside"] = False
            elif move.fromPos.col == 0:
                state["castlingRights"][piece.color]["queenside"] = False

        # pawn promotion
        if piece.pieceType == PieceType.PAWN and (move.toPos.row == 0 or move.toPos.row == 7):
            promotedType = move.promotion if move.promotion else PieceType.QUEEN
            board.setPiece(move.toPos, ChessPiece(promotedType, piece.color, True))

        # en passant capture
        if piece.pieceType == PieceType.PAWN and move.toPos == state["enPassantTarget"]:
            capturedPawnRow = move.fromPos.row
            board.removePiece(chessPosition(capturedPawnRow, move.toPos.col))
            captured = True

        # en passant target
        if piece.pieceType == PieceType.PAWN and abs(move.toPos.row - move.fromPos.row) == 2:
            skippedRow = (move.fromPos.row + move.toPos.row) // 2
            enPassantTarget = chessPosition(skippedRow, move.toPos.col)
        else:
            enPassantTarget = None

        # halfmove clock
        if captured or piece.pieceType == PieceType.PAWN:
            halfmoveClock = 0
        else:
            halfmoveClock = state["halfmoveClock"] + 1

        newColor = Color.BLACK if state["activeColor"] == Color.WHITE else Color.WHITE

        return {
            "board": board,
            "players": state["players"],
            "activeColor": newColor,
            "castlingRights": state["castlingRights"],
            "enPassantTarget": enPassantTarget,
            "halfmoveClock": halfmoveClock,
        }

    def evaluateEnd(self, state: dict) -> Optional[dict]:
        return None