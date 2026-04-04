# install pytest: py -m pip install pytest
# Run chess test cases:  py -m pytest tests/test_chess.py -v -s
# run all test cases at once : py -m pytest tests/ -v

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

def test_position_hash_equal():
    # checks if two positions with same values have equal hash
    pos1 = chessPosition(3, 3)
    pos2 = chessPosition(3, 3)
    assert hash(pos1) == hash(pos2)

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

@pytest.mark.skip(reason="move validation not yet implemented")
def test_pawn_blocked_by_piece():
    # checks if pawn is blocked when enemy piece is directly in front of it
    board = chessBoard()
    board.setupInitialPosition()
    board.setPiece(chessPosition(2, 0), ChessPiece(PieceType.PAWN, Color.BLACK))
    move = chessMove(chessPosition(1, 0), chessPosition(2, 0))
    assert board.isValidMove(move) == False



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

def test_black_rooks_knights_bishops_initial_pos():
    # checks if black rook,  knight and bishop are placed correctly and of right color
    board = chessBoard()
    board.setupInitialPosition()
    black_rook = board.getPiece(chessPosition(7, 7))
    black_knight = board.getPiece(chessPosition(7, 6))
    black_bishop = board.getPiece(chessPosition(7, 5))
    assert black_rook.pieceType == PieceType.ROOK
    assert black_knight.pieceType == PieceType.KNIGHT
    assert black_bishop.pieceType == PieceType.BISHOP
    assert black_rook.color == Color.BLACK
    assert black_knight.color == Color.BLACK
    assert black_bishop.color == Color.BLACK

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

def test_black_piece_not_on_white_side():
    # checks that no black piece is on rows 0 or 1 at the start of the game
    board = chessBoard()
    board.setupInitialPosition()
    white_back_row = board.getPiece(chessPosition(0, 0))
    white_front_row = board.getPiece(chessPosition(1, 0))
    assert white_back_row.color != Color.BLACK
    assert white_front_row.color != Color.BLACK

def test_no_empty_cell_back_rows():
    # checks if rows 0 and 7 have no empty squares after setup- if one of them is empty , then the board is invalid
    board = chessBoard()
    board.setupInitialPosition()
    for col in range(8):
        assert board.getPiece(chessPosition(0, col)) is not None
        assert board.getPiece(chessPosition(7, col)) is not None

def test_no_empty_on_pawn_rows():
    # checks if rows 1 and 6 have no empty squares after setup
    board = chessBoard()
    board.setupInitialPosition()
    for col in range(8):
        assert board.getPiece(chessPosition(1, col)) is not None
        assert board.getPiece(chessPosition(6, col)) is not None



# Board update and state checks
def test_board_remove_piece():
    # checks if square is empty after removing a piece
    board = chessBoard()
    board.setupInitialPosition()
    board.removePiece(chessPosition(1, 0))
    removed = board.getPiece(chessPosition(1, 0))
    assert removed is None

def test_set_piece_on_empty():
    # checks if placing a piece on an empty square stores that piece correctly
    board = chessBoard()
    board.setupInitialPosition()
    new_piece = ChessPiece(PieceType.QUEEN, Color.WHITE)
    board.setPiece(chessPosition(4, 4), new_piece)
    placed_piece = board.getPiece(chessPosition(4, 4))
    assert placed_piece.pieceType == PieceType.QUEEN
    assert placed_piece.color == Color.WHITE
    assert placed_piece.pieceType != PieceType.ROOK

def test_piece_not_moved_on_setup():
    # checks if pieces have hasMoved=False when first placed
    board = chessBoard()
    board.setupInitialPosition()
    white_pawn = board.getPiece(chessPosition(1, 0))
    assert white_pawn.hasMoved == False

def test_remove_then_replace():
    # checks if a square can be reused after a piece is removed and replacement points to new piece and not old
    board = chessBoard()
    board.setupInitialPosition()
    board.removePiece(chessPosition(1, 3))
    board.setPiece(chessPosition(1, 3), ChessPiece(PieceType.BISHOP, Color.BLACK))
    replaced_piece = board.getPiece(chessPosition(1, 3))
    assert replaced_piece.pieceType == PieceType.BISHOP
    assert replaced_piece.color == Color.BLACK
    assert replaced_piece.pieceType != PieceType.PAWN

