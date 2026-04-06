# Run tictactoe model test cases:  py -m pytest src/app/tests/test_tictactoe_models.py -v -s

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.models.tictactoe.TicTacToePosition import TicTacToePosition
from app.models.tictactoe.TicTacToeBoard import TicTacToeBoard
from app.models.tictactoe.TicTacToeMove import TicTacToeMove
from app.models.tictactoe.Player import Player

# Boundary checks
def test_pos_different_row():
    # checks if positions with same col but different row are not equal
    pos1 = TicTacToePosition(0, 2)
    pos2 = TicTacToePosition(1, 2)
    assert pos1 != pos2

def test_pos_row_col_stored_correctly():
    # checks if row and col are stored in correct order and not swapped
    pos = TicTacToePosition(0, 2)
    assert pos.row == 0
    assert pos.col == 2
    assert pos.row != pos.col

def test_pos_hash_equal_position():
    # checks if two equal positions have the same hash value
    pos1 = TicTacToePosition(1, 1)
    pos2 = TicTacToePosition(1, 1)
    assert hash(pos1) == hash(pos2)

#  Board state checks
def test_board_empty_on_start():
    # checks if all cells are None when board is first created
    board = TicTacToeBoard()
    assert board.getCell(TicTacToePosition(0, 0)) is None
    assert board.getCell(TicTacToePosition(1, 1)) is None
    assert board.getCell(TicTacToePosition(2, 2)) is None

def test_board_not_full_empty():
    # checks if empty board is not full
    board = TicTacToeBoard()
    assert board.isFull() == False

def test_board_set_x():
    # checks if setting X stores and retrieves correctly
    board = TicTacToeBoard()
    board.setCell(TicTacToePosition(0, 0), "X")
    cell = board.getCell(TicTacToePosition(0, 0))
    assert cell == "X"
    assert cell != "O"

def test_board_set_o():
    # checks if setting O stores and retrieves correctly
    board = TicTacToeBoard()
    board.setCell(TicTacToePosition(2, 2), "O")
    cell = board.getCell(TicTacToePosition(2, 2))
    assert cell == "O"
    assert cell != "X"

@pytest.mark.skip(reason="written before validation was implemented - test_board_fully_filled covers the real game scenario after validation was added")
def test_board_full_when_filled():
    # checks if board is full when all 9 cells are filled, only checks if isFull returns true when board is full, logic not considered because validation is not implemented
    board = TicTacToeBoard()
    for row in range(3):
        for col in range(3):
            board.setCell(TicTacToePosition(row, col), "X")
    assert board.isFull() == True

def test_board_fully_filled():
    # checks if board is full when all 9 cells are filled with alternating X and O
    board = TicTacToeBoard()
    # fill board alternating X and O like a real game
    values = ["X", "O", "X",
              "O", "X", "O",
              "X", "O", "X"]
    index = 0
    for row in range(3):
        for col in range(3):
            board.setCell(TicTacToePosition(row, col), values[index])
            index += 1
    assert board.isFull() == True

def test_board_cells_independent():
    # checks that setting one cell does not affect other cells
    board = TicTacToeBoard()
    board.setCell(TicTacToePosition(0, 0), "X")
    board.setCell(TicTacToePosition(1, 1), "O")
    board.setCell(TicTacToePosition(2, 2), "X")
    assert board.getCell(TicTacToePosition(0, 0)) == "X"
    assert board.getCell(TicTacToePosition(1, 1)) == "O"
    assert board.getCell(TicTacToePosition(2, 2)) == "X"



def test_board_one_empty_cell():
    # checks if board is not full when one cell is still empty
    board = TicTacToeBoard()
    for row in range(3):
        for col in range(3):
            board.setCell(TicTacToePosition(row, col), "X")
    board.grid[2][2] = None
    assert board.isFull() == False


# Player checks
def test_player_x_val():
    # checks if Player X has been stored correctly
    assert Player.X.value == "X"
    assert Player.X.value != "O"

def test_player_o_val():
    # checks if Player O has been stored correctly
    assert Player.O.value == "O"
    assert Player.O.value != "X"

def test_players_not_equal():
    # checks if X and O are different players
    assert Player.X != Player.O

def test_tictactoe_two_players():
    # checks if there are only two players in tictactoe and not more
    all_players = list(Player)
    assert len(all_players) == 2

def test_board_to_list():
    # verifies that toList() returns a correct list representation of the board
    board = TicTacToeBoard()
    board.setCell(TicTacToePosition(0, 0), "X")
    board.setCell(TicTacToePosition(0, 1), "O")
    board.setCell(TicTacToePosition(1, 1), "X")
    board.setCell(TicTacToePosition(2, 2), "O")

    board_list = board.toList()

    assert board_list == [
        "X", "O", None,
        None, "X", None,
        None, None, "O"
    ]

def test_pos_can_be_used_as_dict_key():
    # verifies that positions with same row and column can be used interchangeably as dictionary keys
    pos1 = TicTacToePosition(2, 2)
    pos2 = TicTacToePosition(2, 2)
    pos_dict = {pos1: "corner"}
    assert pos_dict[pos2] == "corner"