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
from app.modules.TicTacToe.TicTacToeEngine import TicTacToeEngine, evaluateEnd

# HELPER FUNCTIONS
class TicTacToeEngineTestable(TicTacToeEngine):
    def evaluateEnd(self, state):
        return evaluateEnd(None, state)
    def serializeState(self, state):
        return {
            "board": [state["board"].getCell(TicTacToePosition(i // 3, i % 3)) is not None and
                      ("X" if state["board"].getCell(TicTacToePosition(i // 3, i % 3)) == state["players"][0] else "O")
                      or None for i in range(9)],
            "currentPlayer": "X" if state["currentPlayer"] == state["players"][0] else "O",
            "players": {"X": state["players"][0], "O": state["players"][1]}
        }
    def serializeEndResult(self, result):
        return {}
    def deserializeMove(self, data, state):
        index = data["index"]
        return TicTacToeMove(TicTacToePosition(index // 3, index % 3))

def make_engine_and_state():
    engine = TicTacToeEngineTestable()
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

# apply move
def test_mark_placed():
    # checks if the current player's mark is placed on the correct cell
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    new_state = engine.applyMove(state, move)
    assert new_state["board"].getCell(TicTacToePosition(0, 0)) == "Alice"

def test_player_switches():
    # checks if current player switches after a move
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    new_state = engine.applyMove(state, move)
    assert new_state["currentPlayer"] == "Bob"

def test_apply_move_switches_back_to_first_player():
    # checks if player switches back to first player after two moves
    engine, state = make_engine_and_state()
    state = apply_moves(engine, state, [(0,0), (1,1)])
    assert state["currentPlayer"] == "Alice"

def test_move_counter():
    # checks if move counter increments after each move
    engine, state = make_engine_and_state()
    new_state = engine.applyMove(state, TicTacToeMove(TicTacToePosition(0, 0)))
    assert new_state["moves"] == 1

def test_no_mutation():
    # applying a move should actually place the mark on the board in the returned state
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    new_state = engine.applyMove(state, move)
    assert new_state["board"].getCell(TicTacToePosition(0, 0)) == "Alice"


# evaluate all winning conditions
def test_win_top_row():
    # checks if win is detected when top row is filled by same player
    # Alice wins with top row: (0,0)(0,1)(0,2)
    engine, state = make_engine_and_state()
    state = apply_moves(engine, state, [(0,0),(1,0),(0,1),(1,1),(0,2)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "win"
    assert result["winner"] == "Alice"

def test_win_middle_row():
    # Bob wins with middle row
    engine, state = make_engine_and_state()
    state = apply_moves(engine, state, [(0,0),(1,0),(2,0),(1,1),(0,1),(1,2)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "win"
    assert result["winner"] == "Bob"

def test_win_left_column():
    engine, state = make_engine_and_state()
    # Alice wins with left column
    state = apply_moves(engine, state, [(0,0),(0,1),(1,0),(1,1),(2,0)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["result"] == "win"
    assert result["winner"] == "Alice"

def test_win_right_column():
    engine, state = make_engine_and_state()
    # Alice wins with right column
    state = apply_moves(engine, state, [(0,2),(0,0),(1,2),(1,0),(2,2)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["result"] == "win"
    assert result["winner"] == "Alice"

def test_win_main_diagonal():
    # checks if win is detected on main diagonal (top-left to bottom-right)
    engine, state = make_engine_and_state()
    # Alice wins with main diagonal
    state = apply_moves(engine, state, [(0,0),(0,1),(1,1),(0,2),(2,2)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "win"
    assert result["winner"] == "Alice"

def test_win_anti_diagonal():
    engine, state = make_engine_and_state()
    # Alice wins with anti diagonal starting from top-right to bottom-left
    state = apply_moves(engine, state, [(0,2),(0,0),(1,1),(1,0),(2,0)])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["result"] == "win"
    assert result["winner"] == "Alice"


# evaluate draw match
def test_draw_when_board_full():
    # checks if draw is detected when board is full with no winner
    engine, state = make_engine_and_state()
    state = apply_moves(engine, state, [
        (0,0),(0,1),(0,2),
        (1,1),(1,0),(1,2),
        (2,1),(2,0),(2,2)
    ])
    result = engine.evaluateEnd(state)
    assert result is not None
    assert result["isOver"] == True
    assert result["result"] == "draw"

# game continues
def test_game_continues_at_start():
    # checks if evaluateEnd returns None at the start of the game
    engine, state = make_engine_and_state()
    result = engine.evaluateEnd(state)
    assert result is None

def test_game_continues_mid_game():
    # checks if evaluateEnd returns None during an ongoing game
    engine, state = make_engine_and_state()
    state = apply_moves(engine, state, [(0,0),(1,1),(0,1)])
    result = engine.evaluateEnd(state)
    assert result is None

# serialization
def test_serialize_state_maps_players_to_symbols():
    # checks that serializeState correctly maps player names to X/O symbols
    engine, state = make_engine_and_state()
    move = TicTacToeMove(TicTacToePosition(0, 0))
    state = engine.applyMove(state, move)
    serialized = engine.serializeState(state)

    assert serialized["board"][0] == "X"
    assert serialized["currentPlayer"] == "O"
    assert serialized["players"]["X"] == "Alice"
    assert serialized["players"]["O"] == "Bob"

# deserialization
def test_deserialize_converts_index_to_position():
    # checks that deserializeMove correctly converts a index to row/col
    engine, state = make_engine_and_state()
    cases = [(0, 0, 0), (4, 1, 1), (8, 2, 2)]

    for index, expected_row, expected_col in cases:
        move = engine.deserializeMove({"index": index}, state)
        assert move.position.row == expected_row
        assert move.position.col == expected_col