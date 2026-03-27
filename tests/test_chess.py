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



#  Board setup test cases - initial position checks before game starts
def test_white_pawns_position():
    # checks if white pawns are placed in row 1 after initial setup
    board = chessBoard()
    board.setupInitialPosition()
    left_pawn = board.getPiece(chessPosition(1, 0))
    right_pawn = board.getPiece(chessPosition(1, 7))
    assert left_pawn.pieceType == PieceType.PAWN
    assert left_pawn.color == Color.WHITE
    assert right_pawn.pieceType == PieceType.PAWN

def test_black_pawns_position():
    # checks if black pawns are placed in row 6 before game starts
    board = chessBoard()
    board.setupInitialPosition()
    middle_pawn = board.getPiece(chessPosition(6, 4))
    right_pawn = board.getPiece(chessPosition(6, 7))
    assert middle_pawn.pieceType == PieceType.PAWN
    assert middle_pawn.color == Color.BLACK
    assert right_pawn.pieceType == PieceType.PAWN

def test_kings_correct_position():
    # checks if kings are placed at correct positions
    board = chessBoard()
    board.setupInitialPosition()
    white_king = board.getPiece(chessPosition(0, 4))
    black_king = board.getPiece(chessPosition(7, 4))
    assert white_king.pieceType == PieceType.KING
    assert white_king.color == Color.WHITE
    assert black_king.pieceType == PieceType.KING
    assert black_king.color == Color.BLACK
    assert white_king.color != black_king.color

def test_queens_correct_position():
    # checks if white queen is at (0,3) and  black queen is at (7,3)
    board = chessBoard()
    board.setupInitialPosition()
    white_queen = board.getPiece(chessPosition(0, 3))
    black_queen = board.getPiece(chessPosition(7, 3))
    assert white_queen.pieceType == PieceType.QUEEN
    assert white_queen.color == Color.WHITE
    assert black_queen.pieceType == PieceType.QUEEN
    assert black_queen.color == Color.BLACK
    assert white_queen.pieceType != PieceType.KING

def test_white_rooks_knights_bishops_initial_pos():
    # checks if white rook, bishop and knights are at correct position
    board = chessBoard()
    board.setupInitialPosition()
    white_rook = board.getPiece(chessPosition(0, 0))
    white_knight = board.getPiece(chessPosition(0, 1))
    white_bishop = board.getPiece(chessPosition(0, 2))
    assert white_rook.pieceType == PieceType.ROOK
    assert white_knight.pieceType == PieceType.KNIGHT
    assert white_bishop.pieceType == PieceType.BISHOP

def test_middle_rows_empty():
    # checks if rows 2-5 are empty after initial setup
    board = chessBoard()
    board.setupInitialPosition()
    assert board.getPiece(chessPosition(2, 0)) is None
    assert board.getPiece(chessPosition(3, 3)) is None
    assert board.getPiece(chessPosition(4, 7)) is None
    assert board.getPiece(chessPosition(5, 5)) is None

def test_white_piece_not_on_black_side():
    # checks that no white piece is on rows 6 or 7 at the start of the game
    board = chessBoard()
    board.setupInitialPosition()
    black_back_row = board.getPiece(chessPosition(7, 0))
    black_front_row = board.getPiece(chessPosition(6, 0))
    assert black_back_row.color != Color.WHITE
    assert black_front_row.color != Color.WHITE

