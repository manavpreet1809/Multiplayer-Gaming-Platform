from typing import List, Optional
from app.modules.gameEngine import GameEngine
from app.models.chess.chessBoard import ChessBoard
from app.models.chess.chessPiece import Color, PieceType, ChessPiece
from app.models.chess.chessMove import ChessMove
from app.models.chess.chessPosition import ChessPosition

class ChessEngine(GameEngine):
    def createInitialState(self, players: List[str]) -> dict:
        board = ChessBoard()
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

    def validateMove(self, state: dict, move: ChessMove) -> bool:
        if state is None or move is None:
            return False

        if "board" not in state or "activeColor" not in state:
            return False

        board = state["board"]

        if not hasattr(move, "toPos") or move.toPos is None:
            return False

        if not (0 <= move.fromPos.row < 8 and 0 <= move.fromPos.col < 8):
            return False
        if not (0 <= move.toPos.row < 8 and 0 <= move.toPos.col < 8):
            return False

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

    def applyMove(self, state: dict, move: ChessMove) -> dict:
        import copy
        board = state["board"].clone()
        castlingRights = copy.deepcopy(state["castlingRights"])

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
                rook = board.getPiece(ChessPosition(move.fromPos.row, 7))
                board.removePiece(ChessPosition(move.fromPos.row, 7))
                board.setPiece(ChessPosition(move.fromPos.row, 5), rook)
                rook.hasMoved = True
            else:
                # queenside: rook goes from col 0 to col 3
                rook = board.getPiece(ChessPosition(move.fromPos.row, 0))
                board.removePiece(ChessPosition(move.fromPos.row, 0))
                board.setPiece(ChessPosition(move.fromPos.row, 3), rook)
                rook.hasMoved = True
            castlingRights[piece.color]["kingside"] = False
            castlingRights[piece.color]["queenside"] = False

        # revoke castling rights on king/rook move
        if piece.pieceType == PieceType.KING:
            castlingRights[piece.color]["kingside"] = False
            castlingRights[piece.color]["queenside"] = False
        elif piece.pieceType == PieceType.ROOK:
            if move.fromPos.col == 7:
                castlingRights[piece.color]["kingside"] = False
            elif move.fromPos.col == 0:
                castlingRights[piece.color]["queenside"] = False

        # pawn promotion
        if piece.pieceType == PieceType.PAWN and (move.toPos.row == 0 or move.toPos.row == 7):
            promotedType = move.promotion if move.promotion else PieceType.QUEEN
            board.setPiece(move.toPos, ChessPiece(promotedType, piece.color, True))

        # en passant capture
        if piece.pieceType == PieceType.PAWN and move.toPos == state["enPassantTarget"]:
            capturedPawnRow = move.fromPos.row
            capturedPos = ChessPosition(capturedPawnRow, move.toPos.col)
            captured = board.getPiece(capturedPos)
            board.removePiece(capturedPos)

        # en passant target
        if piece.pieceType == PieceType.PAWN and abs(move.toPos.row - move.fromPos.row) == 2:
            skippedRow = (move.fromPos.row + move.toPos.row) // 2
            enPassantTarget = ChessPosition(skippedRow, move.toPos.col)
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
            "castlingRights": castlingRights,
            "enPassantTarget": enPassantTarget,
            "halfmoveClock": halfmoveClock,
        }

    def isLegalMove(self, state: dict, move: ChessMove, piece: ChessPiece, target: Optional[ChessPiece]) -> bool:
        if state is None or move is None or piece is None:
            return False

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
                middle = ChessPosition(move.fromPos.row + direction, move.fromPos.col)
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

    def isPathClear(self, board: ChessBoard, fromPos: ChessPosition, toPos: ChessPosition) -> bool:
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
            if board.getPiece(ChessPosition(r, c)) is not None:
                return False
            r += step_r
            c += step_c
        return True

    def isValidCastle(self, state: dict, move: ChessMove, piece: ChessPiece) -> bool:
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
            rook_pos = ChessPosition(row, 7)
            rook = board.getPiece(rook_pos)
            if rook is None or rook.pieceType != PieceType.ROOK or rook.color != piece.color:
                return False

            # squares between king and rook must be empty
            if board.getPiece(ChessPosition(row, 5)) is not None:
                return False
            if board.getPiece(ChessPosition(row, 6)) is not None:
                return False

            # king cannot pass through or land on attacked squares
            if self.isSquareAttacked(board, ChessPosition(row, 5), opponent):
                return False
            if self.isSquareAttacked(board, ChessPosition(row, 6), opponent):
                return False

            return True

        # queenside
        else:
            # must still have queen side castling rights
            if not state["castlingRights"][piece.color]["queenside"]:
                return False
            # rook must be in correct position
            rook_pos = ChessPosition(row, 0)
            rook = board.getPiece(rook_pos)
            if rook is None or rook.pieceType != PieceType.ROOK or rook.color != piece.color:
                return False

            # squares between king and rook must be empty
            if board.getPiece(ChessPosition(row, 1)) is not None:
                return False
            if board.getPiece(ChessPosition(row, 2)) is not None:
                return False
            if board.getPiece(ChessPosition(row, 3)) is not None:
                return False

            # king cannot pass through or land on attacked squares
            if self.isSquareAttacked(board, ChessPosition(row, 3), opponent):
                return False
            if self.isSquareAttacked(board, ChessPosition(row, 2), opponent):
                return False

            return True

    def cloneState(self, state: dict) -> dict:
        # get current board from the state
        old_board = state["board"]

        # create a brand new empty board
        new_board = ChessBoard()

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
            "enPassantTarget": None if state["enPassantTarget"] is None else ChessPosition(
                state["enPassantTarget"].row,
                state["enPassantTarget"].col
            ),
            "halfmoveClock": state["halfmoveClock"],
        }

    def findKing(self, board: ChessBoard, color: Color) -> ChessPosition:
        # search board
        for r in range(8):
            for c in range(8):
                piece = board.getPiece(ChessPosition(r, c))
                # if piece found is king, return king position
                if piece is not None and piece.color == color and piece.pieceType == PieceType.KING:
                    return ChessPosition(r, c)
        raise ValueError("King not found")

    def isSquareAttacked(self, board: ChessBoard, pos: ChessPosition, attackerColor: Color) -> bool:
        # loop through board
        for r in range(8):
            for c in range(8):

                # potential attacking piece
                attacker_pos = ChessPosition(r, c)
                piece = board.getPiece(attacker_pos)

                # skip if there is no piece or piece is not attacking colour
                if piece is None or piece.color != attackerColor:
                    continue

                # compute distance from target square
                dr = pos.row - r
                dc = pos.col - c

                # Pawn attacks
                if piece.pieceType == PieceType.PAWN:
                    # pawn attacks diagonally forward
                    direction = 1 if piece.color == Color.WHITE else -1

                    # check if pawn can attack target square
                    if dr == direction and abs(dc) == 1:
                        return True

                # Knight attacks
                elif piece.pieceType == PieceType.KNIGHT:
                    # knight moves in L-shape
                    if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
                        return True

                # Bishop attacks
                elif piece.pieceType == PieceType.BISHOP:
                    # Must be diagonal and path must be clear
                    if abs(dr) == abs(dc) and self.isPathClear(board, attacker_pos, pos):
                        return True

                # Rook attacks
                elif piece.pieceType == PieceType.ROOK:
                    # must be straight line and path must be clear
                    if (dr == 0 or dc == 0) and self.isPathClear(board, attacker_pos, pos):
                        return True

                # Queen attacks
                elif piece.pieceType == PieceType.QUEEN:
                    # combination of rook and bishop movement
                    if ((dr == 0 or dc == 0) or abs(dr) == abs(dc)) and self.isPathClear(board, attacker_pos, pos):
                        return True

                # King attacks
                elif piece.pieceType == PieceType.KING:
                    # attacks any adjacent square
                    if max(abs(dr), abs(dc)) == 1:
                        return True

        return False

    def wouldLeaveKingInCheck(self, state: dict, move: ChessMove) -> bool:
        # make copy of current game to test move
        temp_state = self.cloneState(state)

        # create fresh copy of move using fresh position objects (separates simulated move)
        temp_move = ChessMove(
            ChessPosition(move.fromPos.row, move.fromPos.col),
            ChessPosition(move.toPos.row, move.toPos.col),
            move.promotion
        )

        # apply move to copied state
        temp_state = self.applyMove(temp_state, temp_move)

        # colour that made move is activeColour
        moved_color = state["activeColor"]

        # determine opponents colour
        opponent = Color.BLACK if moved_color == Color.WHITE else Color.WHITE

        # find the moved players king on simulated board
        king_pos = self.findKing(temp_state["board"], moved_color)

        # If the opponent attacks the king's square after this move,
        # then the move is illegal because it leaves the king in check
        return self.isSquareAttacked(temp_state["board"], king_pos, opponent)

    def evaluateEnd(self, state: dict) -> Optional[dict]:
        active_color = state["activeColor"]
        board = state["board"]

        # 50 move rule: 100 halfmoves without pawn move or capture
        if state["halfmoveClock"] >= 100:
            return {
                "isOver": True,
                "result": "draw",
                "reason": "50-move rule"
            }

        # find the active players king
        king_pos = self.findKing(board, active_color)

        # determine opponent color
        opponent = Color.BLACK if active_color == Color.WHITE else Color.WHITE

        # is the active player's king currently under attack
        in_check = self.isSquareAttacked(board, king_pos, opponent)

        # does the active player have at least one legal move
        has_legal_move = self.hasAnyLegalMove(state, active_color)

        # checkmate - in check and no legal moves
        if in_check and not has_legal_move:
            winner = Color.BLACK if active_color == Color.WHITE else Color.WHITE
            return {
                "isOver": True,
                "result": "win",
                "winner": winner,
                "reason": "checkmate"
            }

        # stalemate - not in check and no legal moves
        if not in_check and not has_legal_move:
            return {
                "isOver": True,
                "result": "draw",
                "reason": "stalemate"
            }

        # Otherwise game continues
        return None

    def serializeEndResult(self, end_result: dict, state: dict = None) -> dict:
        """Convert evaluateEnd() output to a JSON-serializable dict.

        Converts the Color enum winner to a "white"/"black" string so the
        frontend adapter can determine win/loss/draw relative to the local player.

        Args:
            end_result: output from evaluateEnd()
            state: game state (unused for chess, accepted for polymorphism with TTT)
        """
        if end_result is None:
            return None
        serialized = dict(end_result)
        if "winner" in serialized and serialized["winner"] is not None:
            serialized["winner"] = "white" if serialized["winner"] == Color.WHITE else "black"
        return serialized

    def serializeState(self, state: dict) -> dict:
        """Convert internal state to a JSON-serializable dict for the frontend.

        Handles:
        - Board row-flip (backend row 0 = white's back rank → frontend row 0 = rank 8)
        - Piece objects → single-character codes (uppercase=white, lowercase=black)
        - Color enums → "white"/"black" strings
        - Position objects → {row, col} dicts (in frontend coordinate space)
        """
        board = state["board"]
        active = "white" if state["activeColor"] == Color.WHITE else "black"

        # Convert en-passant target to frontend coords (flip row)
        ep = state["enPassantTarget"]
        en_passant = None
        if ep is not None:
            en_passant = {"row": 7 - ep.row, "col": ep.col}

        return {
            "board": board.toList(),
            "activeColor": active,
            "players": {
                "white": state["players"][Color.WHITE],
                "black": state["players"][Color.BLACK],
            },
            "castlingRights": {
                "white": dict(state["castlingRights"][Color.WHITE]),
                "black": dict(state["castlingRights"][Color.BLACK]),
            },
            "enPassantTarget": en_passant,
            "halfmoveClock": state["halfmoveClock"],
        }

    def deserializeMove(self, move_dict: dict, state: dict = None) -> ChessMove:
        def deserializeMove(self, move_dict: dict, state: dict = None) -> ChessMove:
          """Convert a frontend move dict back to an internal ChessMove.

          Frontend sends {from: {row, col}, to: {row, col}, promotion?: string}
          with row 0 = rank 8.  This flips rows back to backend convention.

          Args:
              move_dict: frontend move payload
              state: game state (unused for chess, accepted for polymorphism with TTT)
          """
          if move_dict is None:
              return None
          if "from" not in move_dict or "to" not in move_dict:
              return None
          if "row" not in move_dict["from"] or "col" not in move_dict["from"]:
              return None
          if "row" not in move_dict["to"] or "col" not in move_dict["to"]:
              return None

        from_pos = ChessPosition(7 - move_dict["from"]["row"], move_dict["from"]["col"])
        to_pos = ChessPosition(7 - move_dict["to"]["row"], move_dict["to"]["col"])

        promotion = None
        if "promotion" in move_dict and move_dict["promotion"]:
            promo_map = {"Q": PieceType.QUEEN, "R": PieceType.ROOK,
                         "B": PieceType.BISHOP, "N": PieceType.KNIGHT}
            promotion = promo_map.get(move_dict["promotion"].upper())

        return ChessMove(from_pos, to_pos, promotion)

    def hasAnyLegalMove(self, state: dict, color: Color) -> bool:
        board = state["board"]

        # temporarily build a state where it is this colors turn,
        # so validateMove checks the correct side.
        test_state = self.cloneState(state)
        test_state["activeColor"] = color

        for from_row in range(8):
            for from_col in range(8):
                from_pos = ChessPosition(from_row, from_col)
                piece = board.getPiece(from_pos)

                # skip empty squares or opponent pieces
                if piece is None or piece.color != color:
                    continue

                # try every destination square on the board
                for to_row in range(8):
                    for to_col in range(8):
                        to_pos = ChessPosition(to_row, to_col)

                        # skip same square moves
                        if from_row == to_row and from_col == to_col:
                            continue

                        # handle normal moves first
                        move = ChessMove(from_pos, to_pos)

                        if self.validateMove(test_state, move):
                            return True

                        # handle promotion moves if a pawn reaches the back rank
                        if piece.pieceType == PieceType.PAWN:
                            last_row = 7 if color == Color.WHITE else 0
                            if to_row == last_row:
                                for promo in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                                    promo_move = ChessMove(from_pos, to_pos, promo)
                                    if self.validateMove(test_state, promo_move):
                                        return True
        return False