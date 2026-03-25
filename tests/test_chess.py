import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'models', 'chess'))

from chessPosition import chessPosition
from chessPiece import ChessPiece, PieceType, Color
from chessBoard import chessBoard
from chessMove import chessMove


# Category 1:  Boundary checks
def test_position_boundaries():
    # lower bound check
    pos_low = chessPosition(0, 0)
    assert pos_low.row == 0
    assert pos_low.col == 0

    # upper bound check
    pos_high = chessPosition(7, 7)
    assert pos_high.row == 7
    assert pos_high.col == 7

    # middle value
    pos_mid = chessPosition(3, 4)
    assert pos_mid.row == 3
    assert pos_mid.col == 4

    # two positions with different values should not be equal
    pos3 = chessPosition(1, 1)
    pos4 = chessPosition(1, 2)
    assert pos3 != pos4