import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'models', 'chess'))

from chessPosition import chessPosition
from chessPiece import ChessPiece, PieceType, Color
from chessBoard import chessBoard
from chessMove import chessMove

#  Boundary checks
def test_position_lower_bound():
    # (0,0) is the minimum valid position on the board
    pos = chessPosition(0, 0)
    assert pos.row == 0
    assert pos.col == 0

def test_position_upper_bound():
    # (7,7) is the maximum valid position on the board
    pos = chessPosition(7, 7)
    assert pos.row == 7
    assert pos.col == 7

def test_position_middle():
    # # Checks if a chessPosition correctly stores row and column values
    pos = chessPosition(3, 4)
    assert pos.row == 3
    assert pos.col == 4

def test_position_equal():
    # two positions with same row and col should be equal
    pos1 = chessPosition(4, 4)
    pos2 = chessPosition(4, 4)
    assert pos1 == pos2

def test_position_different_col():
    # same row but different col should not be equal
    pos1 = chessPosition(1, 1)
    pos2 = chessPosition(1, 2)
    assert pos1 != pos2

@pytest.mark.skip(reason="bounds validation not yet implemented")
def test_position_out_of_bounds():
    with pytest.raises(ValueError):
        chessPosition(8, 8)

