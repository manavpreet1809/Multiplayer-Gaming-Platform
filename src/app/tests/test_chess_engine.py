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






