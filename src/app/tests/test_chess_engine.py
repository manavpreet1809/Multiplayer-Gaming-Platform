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


