# install pytest: py -m pip install pytest
# Run chess engine test cases: py -m pytest src/app/tests/test_chess_engine.py -v -s
# Run all test cases at once: py -m pytest src/app/tests/ -v

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.modules.chess.chessEngine import ChessEngine
from app.models.chess.chessPosition import ChessPosition
from app.models.chess.chessPiece import ChessPiece, PieceType, Color
from app.models.chess.chessBoard import ChessBoard
from app.models.chess.chessMove import ChessMove

# helper function
def make_engine_and_state():
    engine = ChessEngine()
    state = engine.createInitialState(["Alice", "Bob"])
    return engine, state

# initial state
def test_initial_state_white_goes_first():
    # checks if white is the active player at the start of the game
    engine, state = make_engine_and_state()
    assert state["activeColor"] == Color.WHITE

def test_initial_state_players_assigned():
    # checks if players are assigned correctly to white and black
    engine, state = make_engine_and_state()
    assert state["players"][Color.WHITE] == "Alice"
    assert state["players"][Color.BLACK] == "Bob"

def test_initial_state_en_passant_none():
    # checks if en passant target is None at the start of the game
    engine, state = make_engine_and_state()
    assert state["enPassantTarget"] is None

def test_initial_state_halfmove_clock_zero():
    # checks if halfmove clock starts at 0
    engine, state = make_engine_and_state()
    assert state["halfmoveClock"] == 0

def test_initial_state_castling_rights():
    # checks if all castling rights are set to True at the start
    engine, state = make_engine_and_state()
    assert state["castlingRights"][Color.WHITE]["kingside"] == True
    assert state["castlingRights"][Color.WHITE]["queenside"] == True
    assert state["castlingRights"][Color.BLACK]["kingside"] == True
    assert state["castlingRights"][Color.BLACK]["queenside"] == True


# validate moves
def test_validate_empty_square_rejected():
    # checks if moving from an empty square is rejected
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(3, 3), ChessPosition(4, 3))
    assert engine.validateMove(state, move) == False

def test_validate_wrong_turn_rejected():
    # checks if black cannot move on white's turn
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(6, 0), ChessPosition(5, 0))
    assert engine.validateMove(state, move) == False

def test_validate_same_square_rejected():
    # checks if moving to the same square is rejected
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 0), ChessPosition(1, 0))
    assert engine.validateMove(state, move) == False

def test_validate_capture_own_piece_rejected():
    # checks if capturing your own piece is rejected
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 0), ChessPosition(1, 0))
    assert engine.validateMove(state, move) == False

# pawn moves
def test_white_pawn_one_step_forward():
    # checks if white pawn can move one step forward
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 0))
    assert engine.validateMove(state, move) == True

def test_white_pawn_two_steps_from_start():
    # checks if white pawn can move two steps from starting row
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 0), ChessPosition(3, 0))
    assert engine.validateMove(state, move) == True

def test_white_pawn_cannot_move_backward():
    # checks if white pawn cannot move backward
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 0))
    state["board"].setPiece(ChessPosition(3, 0), ChessPiece(PieceType.PAWN, Color.WHITE))
    move = ChessMove(ChessPosition(3, 0), ChessPosition(2, 0))
    assert engine.validateMove(state, move) == False

def test_pawn_diagonal_capture():
    # checks if pawn can capture diagonally
    engine, state = make_engine_and_state()
    state["board"].setPiece(ChessPosition(2, 1), ChessPiece(PieceType.PAWN, Color.BLACK))
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 1))
    assert engine.validateMove(state, move) == True

def test_pawn_cannot_capture_forward():
    # checks if pawn cannot capture a piece directly in front of it and cannot move forward either
    engine, state = make_engine_and_state()
    state["board"].setPiece(ChessPosition(2, 0), ChessPiece(PieceType.PAWN, Color.BLACK))
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 0))
    assert engine.validateMove(state, move) == False

# rook moves
def test_rook_moves_horizontally():
    # checks if rook can move horizontally on an empty row
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 0))
    state["board"].removePiece(ChessPosition(0, 1))
    state["board"].removePiece(ChessPosition(0, 2))
    state["board"].removePiece(ChessPosition(0, 3))
    move = ChessMove(ChessPosition(0, 0), ChessPosition(0, 3))
    assert engine.validateMove(state, move) == True

def test_rook_moves_vertically():
    # checks if rook can move vertically on an empty column
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 0))
    state["board"].removePiece(ChessPosition(2, 0))
    state["board"].removePiece(ChessPosition(3, 0))
    move = ChessMove(ChessPosition(0, 0), ChessPosition(3, 0))
    assert engine.validateMove(state, move) == True

def test_rook_blocked_by_piece():
    # checks if rook is blocked when a piece is in front of it
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 0), ChessPosition(3, 0))
    assert engine.validateMove(state, move) == False

def test_rook_cannot_move_diagonally():
    # checks if rook cannot move diagonally
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 0))
    move = ChessMove(ChessPosition(0, 0), ChessPosition(2, 2))
    assert engine.validateMove(state, move) == False

# bishop moves
def test_bishop_moves_diagonally():
    # checks if bishop can move diagonally on a clear path
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 1))
    state["board"].removePiece(ChessPosition(1, 3))
    move = ChessMove(ChessPosition(0, 2), ChessPosition(2, 4))
    assert engine.validateMove(state, move) == True

def test_bishop_cannot_move_straight():
    # checks if bishop cannot move in a straight line
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 2))
    move = ChessMove(ChessPosition(0, 2), ChessPosition(3, 2))
    assert engine.validateMove(state, move) == False

def test_bishop_blocked_by_piece():
    # checks if bishop is blocked when a piece is in its diagonal path
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 2), ChessPosition(2, 4))
    assert engine.validateMove(state, move) == False


# knight moves
def test_knight_moves_L_shape():
    # checks if knight can move in L-shape
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 1), ChessPosition(2, 2))
    assert engine.validateMove(state, move) == True

def test_knight_jumps_over_pieces():
    # checks if knight can jump over pieces
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 1), ChessPosition(2, 0))
    assert engine.validateMove(state, move) == True

def test_knight_invalid_move():
    # checks if knight cannot move in a non L-shape
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 1), ChessPosition(2, 1))
    assert engine.validateMove(state, move) == False

# queen moves
def test_queen_moves_horizontally():
    # checks if queen can move horizontally
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(0, 2))
    state["board"].removePiece(ChessPosition(0, 1))
    move = ChessMove(ChessPosition(0, 3), ChessPosition(0, 1))
    assert engine.validateMove(state, move) == True

def test_queen_moves_diagonally():
    # checks if queen can move diagonally
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 4))
    move = ChessMove(ChessPosition(0, 3), ChessPosition(2, 5))
    assert engine.validateMove(state, move) == True

def test_queen_moves_vertically():
    # checks if queen can move vertically
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 3))
    move = ChessMove(ChessPosition(0, 3), ChessPosition(2, 3))
    assert engine.validateMove(state, move) == True

def test_queen_blocked_by_piece():
    # checks if queen is blocked when a piece is in its path
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 3), ChessPosition(3, 3))
    assert engine.validateMove(state, move) == False

def test_queen_moves_forward():
    # checks if queen can move forward one step
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 3))
    move = ChessMove(ChessPosition(0, 3), ChessPosition(1, 3))
    assert engine.validateMove(state, move) == True

# check king moves test cases
def test_king_moves_one_square():
    # checks if king can move one square in any direction
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 4))
    move = ChessMove(ChessPosition(0, 4), ChessPosition(1, 4))
    assert engine.validateMove(state, move) == True

def test_king_cannot_move_two_squares():
    # checks if king cannot move two squares without castling
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 4))
    state["board"].removePiece(ChessPosition(2, 4))
    move = ChessMove(ChessPosition(0, 4), ChessPosition(2, 4))
    assert engine.validateMove(state, move) == False

def test_king_cannot_move_into_check():
    # checks if king cannot move into a square attacked by opponent
    engine = ChessEngine()
    board = ChessBoard()
    # white king at (4,4), black rook at (4,7) attacking the row
    board.setPiece(ChessPosition(4, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(4, 7), ChessPiece(PieceType.ROOK, Color.BLACK))
    board.setPiece(ChessPosition(7, 0), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(4, 4), ChessPosition(4, 5))
    assert engine.validateMove(state, move) == False

# castling
def test_kingside_castling_valid():
    # checks if white can castle kingside when path is clear
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(0, 5))
    state["board"].removePiece(ChessPosition(0, 6))
    move = ChessMove(ChessPosition(0, 4), ChessPosition(0, 6))
    assert engine.validateMove(state, move) == True

def test_queenside_castling_valid():
    # checks if white can castle queenside when path is clear
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(0, 1))
    state["board"].removePiece(ChessPosition(0, 2))
    state["board"].removePiece(ChessPosition(0, 3))
    move = ChessMove(ChessPosition(0, 4), ChessPosition(0, 2))
    assert engine.validateMove(state, move) == True

def test_castling_blocked_by_piece():
    # checks if castling is rejected when pieces are in the way
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(0, 4), ChessPosition(0, 6))
    assert engine.validateMove(state, move) == False

def test_castling_rights_revoked_after_king_moves():
    # checks if castling rights are revoked after king moves
    engine, state = make_engine_and_state()
    state["board"].removePiece(ChessPosition(1, 4))
    move = ChessMove(ChessPosition(0, 4), ChessPosition(1, 4))
    new_state = engine.applyMove(state, move)
    assert new_state["castlingRights"][Color.WHITE]["kingside"] == False
    assert new_state["castlingRights"][Color.WHITE]["queenside"] == False


# en passant
def test_en_passant_target_set():
    # when a pawn jumps two squares forward, the square it skipped over should be saved as the en passant target
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 4), ChessPosition(3, 4))
    new_state = engine.applyMove(state, move)
    assert new_state["enPassantTarget"] == ChessPosition(2, 4)

def test_en_passant_capture():
    # white pawn should be able to capture diagonally behind the black pawn that just double moved
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(4, 4), ChessPiece(PieceType.PAWN, Color.WHITE))
    board.setPiece(ChessPosition(4, 5), ChessPiece(PieceType.PAWN, Color.BLACK))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(7, 4), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": ChessPosition(5, 5),
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(4, 4), ChessPosition(5, 5))
    assert engine.validateMove(state, move) == True

# pawn promotion test cases
def test_pawn_promotion_to_rook():
    #  checks that pawn can promote to a rook
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(6, 0), ChessPiece(PieceType.PAWN, Color.WHITE))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(7, 4), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(6, 0), ChessPosition(7, 0), PieceType.ROOK)
    new_state = engine.applyMove(state, move)
    promoted = new_state["board"].getPiece(ChessPosition(7, 0))
    assert promoted.pieceType == PieceType.ROOK
    assert promoted.color == Color.WHITE

def test_pawn_promotion_default_queen():
    # checks if pawn promotes to queen by default when no promotion specified
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(6, 0), ChessPiece(PieceType.PAWN, Color.WHITE))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(7, 4), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(6, 0), ChessPosition(7, 0))
    new_state = engine.applyMove(state, move)
    promoted = new_state["board"].getPiece(ChessPosition(7, 0))
    assert promoted.pieceType == PieceType.QUEEN

def test_turn_switches_after_move():
    # checks if turn switches from white to black after white makes a move
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 0))
    new_state = engine.applyMove(state, move)
    assert new_state["activeColor"] == Color.BLACK

def test_halfmove_clock_increments():
    # halfmove clock should go up by 1 when no pawn moved and nothing got captured
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(4, 4), ChessPiece(PieceType.ROOK, Color.WHITE))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(7, 4), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(4, 4), ChessPosition(4, 5))
    new_state = engine.applyMove(state, move)
    assert new_state["halfmoveClock"] == 1

def test_halfmove_clock_resets_on_pawn_move():
    # checks if halfmove clock resets to 0 after a pawn move
    engine, state = make_engine_and_state()
    state["halfmoveClock"] = 10
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 0))
    new_state = engine.applyMove(state, move)
    assert new_state["halfmoveClock"] == 0

def test_piece_marked_as_moved():
    # checks if piece hasMoved flag is set to True after moving
    engine, state = make_engine_and_state()
    move = ChessMove(ChessPosition(1, 0), ChessPosition(2, 0))
    new_state = engine.applyMove(state, move)
    piece = new_state["board"].getPiece(ChessPosition(2, 0))
    assert piece.hasMoved == True

def test_capture_removes_opponent_piece():
    # checks if capturing an opponent piece removes it from the board
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(4, 4), ChessPiece(PieceType.ROOK, Color.WHITE))
    board.setPiece(ChessPosition(4, 7), ChessPiece(PieceType.PAWN, Color.BLACK))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(7, 4), ChessPiece(PieceType.KING, Color.BLACK))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.WHITE,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    move = ChessMove(ChessPosition(4, 4), ChessPosition(4, 7))
    new_state = engine.applyMove(state, move)
    piece = new_state["board"].getPiece(ChessPosition(4, 7))
    assert piece.pieceType == PieceType.ROOK
    assert piece.color == Color.WHITE

#checkmate
def test_checkmate_detected():
    ## checks if the engine correctly identifies a checkmate situation and declares a win
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(7, 7), ChessPiece(PieceType.KING, Color.BLACK))
    board.setPiece(ChessPosition(0, 4), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(6, 5), ChessPiece(PieceType.QUEEN, Color.WHITE))
    board.setPiece(ChessPosition(5, 7), ChessPiece(PieceType.ROOK, Color.WHITE))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.BLACK,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "win"
    assert result["winner"] == Color.WHITE


# stalemate
def test_stalemate_detected():
    # checks if the engine correctly identifies a stalemate situation and declares a draw
    engine = ChessEngine()
    board = ChessBoard()
    board.setPiece(ChessPosition(7, 7), ChessPiece(PieceType.KING, Color.BLACK))
    board.setPiece(ChessPosition(5, 6), ChessPiece(PieceType.KING, Color.WHITE))
    board.setPiece(ChessPosition(6, 5), ChessPiece(PieceType.QUEEN, Color.WHITE))
    state = {
        "board": board,
        "players": {Color.WHITE: "Alice", Color.BLACK: "Bob"},
        "activeColor": Color.BLACK,
        "castlingRights": {Color.WHITE: {"kingside": False, "queenside": False},
                           Color.BLACK: {"kingside": False, "queenside": False}},
        "enPassantTarget": None,
        "halfmoveClock": 0,
    }
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "draw"
    assert result["reason"] == "stalemate"


# fifty move rule
def test_fifty_move_rule_draw():
    # checks if the game ends in a draw when 50-move rule (100 half moves) is reached
    engine, state = make_engine_and_state()
    state["halfmoveClock"] = 100
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "draw"
    assert result["reason"] == "50-move rule"






