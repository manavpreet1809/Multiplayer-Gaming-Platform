from typing import List, Optional
from modules.gameEngine import GameEngine
from app.models.chess.chessBoard import chessBoard
from app.models.chess.chessPiece import Color
from app.models.chess.chessMove import chessMove

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

        board.removePiece(move.fromPos)
        board.setPiece(move.toPos, piece)
        piece.hasMoved = True

        newColor = Color.BLACK if state["activeColor"] == Color.WHITE else Color.WHITE

        return {
            "board": board,
            "players": state["players"],
            "activeColor": newColor,
            "castlingRights": state["castlingRights"],
            "enPassantTarget": None,  # TODO: set if pawn double-push
            "halfmoveClock": state["halfmoveClock"] + 1,  # TODO: reset on pawn move/capture
        }

    def evaluateEnd(self, state: dict) -> Optional[dict]:
        return None