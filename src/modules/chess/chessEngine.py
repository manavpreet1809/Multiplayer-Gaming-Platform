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
        board = state["board"]
        piece = board.getPiece(move.fromPos)
        target = board.getPiece(move.toPos)

        if piece is None:
            return False

        if piece.color != state["activeColor"]:
            return False

        if move.fromPos == move.toPos:
            return False

        if target is not None and target.color == piece.color:
            return False

        if not self.isLegalMove(state, move, piece, target):
            return False

        if self.wouldLeaveKingInCheck(state, move):
            return False

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

    def isLegalMove(self, state: dict, move: chessMove, piece: ChessPiece, target: Optional[ChessPiece]) -> bool:
        board = state["board"]
        # change in row/ col (delta row, delta column)
        dr = move.toPos.row - move.fromPos.row
        dc = move.toPos.col - move.fromPos.col

        # check rook movement (move in straight line)
        if piece.pieceType == PieceType.ROOK:
            if dr != 0 and dc != 0:
                return False
            return self.isPathClear(board, move.fromPos, move.toPos)

        # check bishop movement (must move diagonally)
        if piece.pieceType == PieceType.BISHOP:
            if abs(dr) != abs(dc):
                return False
            return self.isPathClear(board, move.fromPos, move.toPos)

        # check queen movement (rook or bishop movement)
        if piece.pieceType == PieceType.QUEEN:
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                return self.isPathClear(board, move.fromPos, move.toPos)
            return False

        # check knight movement (2,1) or (1,2), ignores blocking
        if piece.pieceType == PieceType.KNIGHT:
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]

        # check King movement (one square in any direction or castling)
        if piece.pieceType == PieceType.KING:
            if max(abs(dr), abs(dc)) == 1:
                return True
            if dr == 0 and abs(dc) == 2:
                return self.isValidCastle(state, move, piece)
            return False

        # check pawn movement (white pawn moves in pos row direction, black pawn in negative row direction)
        if piece.pieceType == PieceType.PAWN:
            direction = 1 if piece.color == Color.WHITE else -1
            start_row = 1 if piece.color == Color.WHITE else 6
            last_row = 7 if piece.color == Color.WHITE else 0

            # one square forward
            if dc == 0 and dr == direction and target is None:
                # move promotion
                if move.toPos.row == last_row:
                    return move.promotion in [None, PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]
                return move.promotion is None

            # two squares forward
            if dc == 0 and dr == 2 * direction and move.fromPos.row == start_row:
                middle = chessPosition(move.fromPos.row + direction, move.fromPos.col)
                if board.getPiece(middle) is None and target is None:
                    return move.promotion is None
                return False

            # diagonal capture
            if abs(dc) == 1 and dr == direction and target is not None and target.color != piece.color:
                # move promotion
                if move.toPos.row == last_row:
                    return move.promotion in [None, PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]
                return move.promotion is None

            # en passant
            if abs(dc) == 1 and dr == direction and target is None:
                if state["enPassantTarget"] is not None and move.toPos == state["enPassantTarget"]:
                    return move.promotion is None

            return False

        return False

    def isPathClear(self, board: chessBoard, fromPos: chessPosition, toPos: chessPosition) -> bool:
        # Compute how far we are moving in rows and columns
        dr = toPos.row - fromPos.row
        dc = toPos.col - fromPos.col

        # Determine direction of movement:
        # step_r will be -1, 0, or 1 depending on direction in rows
        # step_c will be -1, 0, or 1 depending on direction in columns
        step_r = 0 if dr == 0 else dr // abs(dr)
        step_c = 0 if dc == 0 else dc // abs(dc)

        # Start from the square immediately after the starting position
        r = fromPos.row + step_r
        c = fromPos.col + step_c

        # Walk along the path toward the destination square
        while r != toPos.row or c != toPos.col:
            # If any square in between has a piece, path is blocked
            if board.getPiece(chessPosition(r, c)) is not None:
                return False
            r += step_r
            c += step_c
        return True

    def isValidCastle(self, state: dict, move: chessMove, piece: ChessPiece) -> bool:
        board = state["board"]
        row = move.fromPos.row
        opponent = Color.BLACK if piece.color == Color.WHITE else Color.WHITE

        # king must not have moved before
        if piece.hasMoved:
            return False

        # king cannot currently be in check
        if self.isSquareAttacked(board, move.fromPos, opponent):
            return False

        # kingside
        if move.toPos.col > move.fromPos.col:
            if not state["castlingRights"][piece.color]["kingside"]:
                return False

            # rook must be in correct position
            rook_pos = chessPosition(row, 7)
            rook = board.getPiece(rook_pos)
            if rook is None or rook.pieceType != PieceType.ROOK or rook.color != piece.color:
                return False

            # squares between king and rook must be empty
            if board.getPiece(chessPosition(row, 5)) is not None:
                return False
            if board.getPiece(chessPosition(row, 6)) is not None:
                return False

            # king cannot pass through or land on attacked squares
            if self._isSquareAttacked(board, chessPosition(row, 5), opponent):
                return False
            if self._isSquareAttacked(board, chessPosition(row, 6), opponent):
                return False

            return True

        # queenside
        else:
            # must still have queen side castling rights
            if not state["castlingRights"][piece.color]["queenside"]:
                return False
            # rook must be in correct position
            rook_pos = chessPosition(row, 0)
            rook = board.getPiece(rook_pos)
            if rook is None or rook.pieceType != PieceType.ROOK or rook.color != piece.color:
                return False

            # squares between king and rook must be empty
            if board.getPiece(chessPosition(row, 1)) is not None:
                return False
            if board.getPiece(chessPosition(row, 2)) is not None:
                return False
            if board.getPiece(chessPosition(row, 3)) is not None:
                return False

            # king cannot pass through or land on attacked squares
            if self.isSquareAttacked(board, chessPosition(row, 3), opponent):
                return False
            if self.isSquareAttacked(board, chessPosition(row, 2), opponent):
                return False

            return True

    def cloneState(self, state: dict) -> dict:
        # get current board from the state
        old_board = state["board"]

        # create a brand new empty baord
        new_board = chessBoard()

        # loop through every square on board
        for r in range(8):
            for c in range(8):

                # get piece at this position from original board
                piece = old_board.grid[r][c]

                # if there is a piece, copy it to new board
                if piece is not None:
                    new_board.grid[r][c] = ChessPiece(piece.pieceType, piece.color, piece.hasMoved)

        # return new state dictionary
        return {

            # use newly cloned board + copy player mapping
            "board": new_board,
            "players": dict(state["players"]),
            "activeColor": state["activeColor"],

            # copy castling rights
            "castlingRights": {
                Color.WHITE: dict(state["castlingRights"][Color.WHITE]),
                Color.BLACK: dict(state["castlingRights"][Color.BLACK]),
            },

            # copy en passant target position, if it exists
            "enPassantTarget": None if state["enPassantTarget"] is None else chessPosition(
                state["enPassantTarget"].row,
                state["enPassantTarget"].col
            ),
            "halfmoveClock": state["halfmoveClock"],
        }

    def findKing(self, board: chessBoard, color: Color) -> chessPosition:
        # search board
        for r in range(8):
            for c in range(8):
                piece = board.getPiece(chessPosition(r, c))
                # if piece found is king, return king position
                if piece is not None and piece.color == color and piece.pieceType == PieceType.KING:
                    return chessPosition(r, c)
        raise ValueError("King not found")


    def evaluateEnd(self, state: dict) -> Optional[dict]:
        return None