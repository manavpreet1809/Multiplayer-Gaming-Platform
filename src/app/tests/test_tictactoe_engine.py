# install pytest: py -m pip install pytest
# Run tictactoe engine test cases: py -m pytest src/app/tests/test_tictactoe_engine.py -v -s
# Run all test cases at once: py -m pytest src/app/tests/ -v

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.modules.TicTacToe.TicTacToeEngine import TicTacToeEngine
from app.models.tictactoe.TicTacToeMove import TicTacToeMove
from app.models.tictactoe.TicTacToePosition import TicTacToePosition
from app.models.tictactoe.TicTacToeBoard import TicTacToeBoard

# HELPER FUNCTIONS
def make_engine_and_state():
    engine = TicTacToeEngine()
    state = engine.createInitialState(["Alice", "Bob"])
    return engine, state

def apply_moves(engine, state, moves):
    # applies a list of moves one by one and returns the updated board state
    for row, col in moves:
        move = TicTacToeMove(TicTacToePosition(row, col))
        state = engine.applyMove(state, move)
    return state


# initial state checks
def test_initial_state_first_player():
    # checks if first player is set as current player at start
    engine, state = make_engine_and_state()
    assert state["currentPlayer"] == "Alice"

def test_initial_state_moves_zero():
    # checks if move counter starts at 0
    engine, state = make_engine_and_state()
    assert state["moves"] == 0

def test_initial_state_players_assigned():
    # checks if both players are assigned correctly
    engine, state = make_engine_and_state()
    assert state["players"][0] == "Alice"
    assert state["players"][1] == "Bob"


# validate move
def test_validate_empty_cell_valid():
    # checks if placing on an empty cell is valid
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    assert engine.validateMove(state, move) == True

def test_validate_occupied_cell_rejected():
    # checks if placing on an already occupied cell is rejected
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    state = engine.applyMove(state, move)
    assert engine.validateMove(state, move) == False

def test_validate_out_of_bounds_rejected():
    # checks if placing outside the 3x3 board is rejected
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(3, 3))
    assert engine.validateMove(state, move) == False

def test_validate_negative_position_rejected():
    # checks if negative position is rejected
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(-1, 0))
    assert engine.validateMove(state, move) == False

def test_all_corners_valid():
    # checks if all four corners are valid moves on empty board
    engine, state = make_engine_and_state()
    corners = [(0,0), (0,2), (2,0), (2,2)]
    for row, col in corners:
        move = TicTacToeMove(TicTacToePosition(row, col))
        assert engine.validateMove(state, move) == True

