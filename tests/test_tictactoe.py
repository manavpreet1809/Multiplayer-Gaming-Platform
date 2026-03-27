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
