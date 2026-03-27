import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'models', 'tictactoe'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from TicTacToePosition import TicTacToePosition
from Player import Player
from TicTacToeBoard import TicTacToeBoard
from TicTacToeMove import TicTacToeMove

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


def test_board_full_when_filled():
    # checks if board is full when all 9 cells are filled, only checks if isFull returns true when board is full, logic not considered because validation is not implemented
    board = TicTacToeBoard()
    for row in range(3):
        for col in range(3):
            board.setCell(TicTacToePosition(row, col), "X")
    assert board.isFull() == True


@pytest.mark.skip(reason="turn validation not yet implemented")
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
