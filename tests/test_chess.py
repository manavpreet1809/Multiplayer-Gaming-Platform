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
    # Checks if a chessPosition correctly stores row and column values
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


# Move checks
def test_move_from_position():
    # checking fromPos is stored correctly
    move = chessMove(chessPosition(1, 0), chessPosition(3, 0))
    assert move.fromPos.row == 1
    assert move.fromPos.col == 0

def test_move_to_position():
    # checking toPos is stored correctly
    move = chessMove(chessPosition(1, 0), chessPosition(3, 0))
    assert move.toPos.row == 3
    assert move.toPos.col == 0

def test_move_diff_square():
    #  from and to positions should not be the same square for a valid move
    pawn_move = chessMove(chessPosition(1, 0), chessPosition(3, 0))
    assert pawn_move.fromPos != pawn_move.toPos

def test_no_promo_default():
    # checks that a regular move has no promotion
    move = chessMove(chessPosition(4, 4), chessPosition(5, 4))
    assert move.promotion is None

def test_promo_queen():
    # checks that pawn promoting to queen is stored correctly and not with other types
    queen_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.QUEEN)
    assert queen_promo.promotion == PieceType.QUEEN
    assert queen_promo.promotion != PieceType.ROOK

def test_promo_knight():
    # checks that pawn promoting to knight is stored correctly
    knight_promo = chessMove(chessPosition(6, 3), chessPosition(7, 3), promotion=PieceType.KNIGHT)
    assert knight_promo.promotion == PieceType.KNIGHT
    assert knight_promo.promotion != PieceType.QUEEN

def test_diff_promos_not_equal():
    # checks that bishop and rook are two different promotions and are not equal
    bishop_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.BISHOP)
    rook_promo = chessMove(chessPosition(6, 0), chessPosition(7, 0), promotion=PieceType.ROOK)
    assert bishop_promo.promotion != rook_promo.promotion

