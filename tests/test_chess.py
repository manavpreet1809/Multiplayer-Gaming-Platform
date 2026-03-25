import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'models', 'chess'))

from chessPosition import chessPosition
from chessPiece import ChessPiece, PieceType, Color
from chessBoard import chessBoard
from chessMove import chessMove


# Boundary checks
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


# Move checks
def test_valid_moves():
    # basic chess move should store from and to positions correctly
    move1 = chessMove(chessPosition(1, 0), chessPosition(3, 0))
    assert move1.fromPos.row == 1
    assert move1.fromPos.col == 0
    assert move1.toPos.row == 3
    assert move1.toPos.col == 0

    # from and to should be at different positions
    pawn_move = chessMove(chessPosition(1, 0), chessPosition(3, 0))
    assert pawn_move.fromPos != pawn_move.toPos

    queen_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.QUEEN)
    assert queen_promo.promotion == PieceType.QUEEN
    assert queen_promo.promotion != PieceType.ROOK

    # two different promotions should not be equal
    bishop_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.BISHOP)
    knight_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.KNIGHT)
    assert bishop_promo.promotion != knight_promo.promotion