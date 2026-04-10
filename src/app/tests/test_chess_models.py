# install pytest: py -m pip install pytest
# Run chess model test cases:  py -m pytest src/app/tests/test_chess_models.py -v -s
# Run all test cases at once:  py -m pytest src/app/tests/ -v

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.models.chess.chessPosition import ChessPosition
from app.models.chess.chessPiece import ChessPiece, PieceType, Color
from app.models.chess.chessBoard import ChessBoard
from app.models.chess.chessMove import ChessMove


# verifies that toList() correctly represents a mid-game board state
def test_chess_to_list_mid_game():
    board = ChessBoard()
    board.setupInitialPosition()

    pawn = board.getPiece(ChessPosition(1, 4))
    board.removePiece(ChessPosition(1, 4))
    board.setPiece(ChessPosition(3, 4), pawn)
    board.removePiece(ChessPosition(7, 6))
    board.setPiece(ChessPosition(4, 4), ChessPiece(PieceType.QUEEN, Color.WHITE))

    board_list = board.toList()
    assert board_list == [
        ["r", "n", "b", "q", "k", "b", None, "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, "Q", None, None, None],
        [None, None, None, None, "P", None, None, None],
        [None, None, None, None, None, None, None, None],
        ["P", "P", "P", "P", None, "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]

#  Boundary checks
def test_position_lower_bound():
    # (0,0) is the minimum valid position on the board
    pos = ChessPosition(0, 0)
    assert pos.row == 0
    assert pos.col == 0

def test_position_upper_bound():
    # (7,7) is the maximum valid position on the board
    pos = ChessPosition(7, 7)
    assert pos.row == 7
    assert pos.col == 7

def test_position_middle():
    # Checks if a ChessPosition correctly stores row and column values
    pos = ChessPosition(3, 4)
    assert pos.row == 3
    assert pos.col == 4

def test_position_equal():
    # two positions with same row and col should be equal
    pos1 = ChessPosition(4, 4)
    pos2 = ChessPosition(4, 4)
    assert pos1 == pos2

def test_position_different_col():
    # same row but different col should not be equal
    pos1 = ChessPosition(1, 1)
    pos2 = ChessPosition(1, 2)
    assert pos1 != pos2

def test_position_hash_equal():
    # checks if two positions with same values have equal hash
    pos1 = ChessPosition(3, 3)
    pos2 = ChessPosition(3, 3)
    assert hash(pos1) == hash(pos2)


def test_invalid_position():
    # checks that invalid positions raise ValueError
    with pytest.raises(ValueError):
        ChessPosition(8, 0)
    with pytest.raises(ValueError):
        ChessPosition(0, 8)
    with pytest.raises(ValueError):
        ChessPosition(-1, 0)
    with pytest.raises(ValueError):
            ChessPosition(8, 8)


# Move checks
def test_move_from_position():
    # checking fromPos is stored correctly
    move = ChessMove(ChessPosition(1, 0), ChessPosition(3, 0))
    assert move.fromPos.row == 1
    assert move.fromPos.col == 0

def test_move_to_position():
    # checking toPos is stored correctly
    move = ChessMove(ChessPosition(1, 0), ChessPosition(3, 0))
    assert move.toPos.row == 3
    assert move.toPos.col == 0

def test_move_diff_square():
    #  from and to positions should not be the same square for a valid move
    pawn_move = ChessMove(ChessPosition(1, 0), ChessPosition(3, 0))
    assert pawn_move.fromPos != pawn_move.toPos

def test_no_promo_default():
    # checks that a regular move has no promotion
    move = ChessMove(ChessPosition(4, 4), ChessPosition(5, 4))
    assert move.promotion is None

def test_promo_queen():
    # checks that pawn promoting to queen is stored correctly and not with other types
    queen_promo = ChessMove(ChessPosition(6, 0), ChessPosition(7, 0), promotion=PieceType.QUEEN)
    assert queen_promo.promotion == PieceType.QUEEN
    assert queen_promo.promotion != PieceType.ROOK

def test_promo_knight():
    # checks that pawn promoting to knight is stored correctly
    knight_promo = ChessMove(ChessPosition(6, 3), ChessPosition(7, 3), promotion=PieceType.KNIGHT)
    assert knight_promo.promotion == PieceType.KNIGHT
    assert knight_promo.promotion != PieceType.QUEEN

def test_diff_promos_not_equal():
    # checks that bishop and rook are two different promotions and are not equal
    bishop_promo = ChessMove(ChessPosition(6, 0), ChessPosition(7, 0), promotion=PieceType.BISHOP)
    rook_promo = ChessMove(ChessPosition(6, 0), ChessPosition(7, 0), promotion=PieceType.ROOK)
    assert bishop_promo.promotion != rook_promo.promotion


#  Board setup test cases - initial position checks before game starts
def test_white_pawns_position():
    # checks if white pawns are placed in row 1 after initial setup
    board = ChessBoard()
    board.setupInitialPosition()
    for col in range(8):
        piece = board.getPiece(ChessPosition(1, col))
        assert piece is not None
        assert piece.pieceType == PieceType.PAWN
        assert piece.color == Color.WHITE

def test_black_pawns_position():
    # checks if black pawns are placed in row 6 before game starts
    board = ChessBoard()
    board.setupInitialPosition()
    for col in range(8):
        piece = board.getPiece(ChessPosition(6, col))
        assert piece is not None
        assert piece.pieceType == PieceType.PAWN
        assert piece.color == Color.BLACK

def test_kings_correct_position():
    # checks if kings are placed at correct positions
    board = ChessBoard()
    board.setupInitialPosition()
    white_king = board.getPiece(ChessPosition(0, 4))
    black_king = board.getPiece(ChessPosition(7, 4))
    assert white_king.pieceType == PieceType.KING
    assert white_king.color == Color.WHITE
    assert black_king.pieceType == PieceType.KING
    assert black_king.color == Color.BLACK
    assert white_king.color != black_king.color

def test_queens_correct_position():
    # checks if white queen is at (0,3) and  black queen is at (7,3)
    board = ChessBoard()
    board.setupInitialPosition()
    white_queen = board.getPiece(ChessPosition(0, 3))
    black_queen = board.getPiece(ChessPosition(7, 3))
    assert white_queen.pieceType == PieceType.QUEEN
    assert white_queen.color == Color.WHITE
    assert black_queen.pieceType == PieceType.QUEEN
    assert black_queen.color == Color.BLACK
    assert white_queen.pieceType != PieceType.KING

def test_white_rooks_knights_bishops_initial_pos():
    # checks if white rook, bishop and knights are at correct position
    board = ChessBoard()
    board.setupInitialPosition()
    white_rook = board.getPiece(ChessPosition(0, 0))
    white_knight = board.getPiece(ChessPosition(0, 1))
    white_bishop = board.getPiece(ChessPosition(0, 2))
    assert white_rook.pieceType == PieceType.ROOK
    assert white_knight.pieceType == PieceType.KNIGHT
    assert white_bishop.pieceType == PieceType.BISHOP

def test_black_rooks_knights_bishops_initial_pos():
    # checks if black rook,  knight and bishop are placed correctly and of right color
    board = ChessBoard()
    board.setupInitialPosition()
    black_rook = board.getPiece(ChessPosition(7, 7))
    black_knight = board.getPiece(ChessPosition(7, 6))
    black_bishop = board.getPiece(ChessPosition(7, 5))
    assert black_rook.pieceType == PieceType.ROOK
    assert black_knight.pieceType == PieceType.KNIGHT
    assert black_bishop.pieceType == PieceType.BISHOP
    assert black_rook.color == Color.BLACK
    assert black_knight.color == Color.BLACK
    assert black_bishop.color == Color.BLACK

def test_all_middle_rows_empty():
    # checks if all squares in rows 2-5 are empty after initial setup
    board = ChessBoard()
    board.setupInitialPosition()
    for row in range(2, 6):
        for col in range(8):
            assert board.getPiece(ChessPosition(row, col)) is None



def test_white_piece_not_on_black_side():
    # checks that no white piece is on rows 6 or 7 at the start of the game
    board = ChessBoard()
    board.setupInitialPosition()
    black_back_row = board.getPiece(ChessPosition(7, 0))
    black_front_row = board.getPiece(ChessPosition(6, 0))
    assert black_back_row.color != Color.WHITE
    assert black_front_row.color != Color.WHITE

def test_black_piece_not_on_white_side():
    # checks that no black piece is on rows 0 or 1 at the start of the game
    board = ChessBoard()
    board.setupInitialPosition()
    white_back_row = board.getPiece(ChessPosition(0, 0))
    white_front_row = board.getPiece(ChessPosition(1, 0))
    assert white_back_row.color != Color.BLACK
    assert white_front_row.color != Color.BLACK

def test_no_empty_cell_back_rows():
    # checks if rows 0 and 7 have no empty squares after setup- if one of them is empty , then the board is invalid
    board = ChessBoard()
    board.setupInitialPosition()
    for col in range(8):
        assert board.getPiece(ChessPosition(0, col)) is not None
        assert board.getPiece(ChessPosition(7, col)) is not None

def test_no_empty_on_pawn_rows():
    # checks if rows 1 and 6 have no empty squares after setup
    board = ChessBoard()
    board.setupInitialPosition()
    for col in range(8):
        assert board.getPiece(ChessPosition(1, col)) is not None
        assert board.getPiece(ChessPosition(6, col)) is not None


# Board update and state checks
def test_board_remove_piece():
    # checks if square is empty after removing a piece
    board = ChessBoard()
    board.setupInitialPosition()
    board.removePiece(ChessPosition(1, 0))
    removed = board.getPiece(ChessPosition(1, 0))
    assert removed is None

def test_set_piece_on_empty():
    # checks if placing a piece on an empty square stores that piece correctly
    board = ChessBoard()
    board.setupInitialPosition()
    new_piece = ChessPiece(PieceType.QUEEN, Color.WHITE)
    board.setPiece(ChessPosition(4, 4), new_piece)
    placed_piece = board.getPiece(ChessPosition(4, 4))
    assert placed_piece.pieceType == PieceType.QUEEN
    assert placed_piece.color == Color.WHITE
    assert placed_piece.pieceType != PieceType.ROOK

def test_piece_not_moved_on_setup():
    # checks if pieces have hasMoved=False when first placed
    board = ChessBoard()
    board.setupInitialPosition()
    white_pawn = board.getPiece(ChessPosition(1, 0))
    assert white_pawn.hasMoved == False

def test_remove_then_replace():
    # checks if a square can be reused after a piece is removed and replacement points to new piece and not old
    board = ChessBoard()
    board.setupInitialPosition()
    board.removePiece(ChessPosition(1, 3))
    board.setPiece(ChessPosition(1, 3), ChessPiece(PieceType.BISHOP, Color.BLACK))
    replaced_piece = board.getPiece(ChessPosition(1, 3))
    assert replaced_piece.pieceType == PieceType.BISHOP
    assert replaced_piece.color == Color.BLACK
    assert replaced_piece.pieceType != PieceType.PAWN

def test_piece_code():
    # white pieces should return uppercase letter codes
    # black pieces should return lowercase letter codes

    # king codes
    white_king = ChessPiece(PieceType.KING, Color.WHITE)
    black_king = ChessPiece(PieceType.KING, Color.BLACK)
    assert white_king.toCode() == "K"   # white king → "K"
    assert black_king.toCode() == "k"   # black king → "k"

    # pawn codes
    white_pawn = ChessPiece(PieceType.PAWN, Color.WHITE)
    black_pawn = ChessPiece(PieceType.PAWN, Color.BLACK)
    assert white_pawn.toCode() == "P"   # white pawn → "P"
    assert black_pawn.toCode() == "p"   # black pawn → "p"

def test_board_clone():
    # checks that modifying clone does not affect original board
    board = ChessBoard()
    board.setupInitialPosition()
    clone = board.clone()
    clone.removePiece(ChessPosition(1, 0))  # removing the pawn from clone
    assert board.getPiece(ChessPosition(1, 0)) is not None # original board should still have the pawn
    assert clone.getPiece(ChessPosition(1, 0)) is None  # pawn removed from cloned board

def test_clone_modifying_piece_does_not_affect_original():
    #  ensures modifying a piece in the cloned board does not affect the original
    board = ChessBoard()
    board.setupInitialPosition()
    clone = board.clone()
    pawn_clone = clone.getPiece(ChessPosition(1,0))
    pawn_clone.hasMoved = True
    assert board.getPiece(ChessPosition(1,0)).hasMoved == False

def test_position_equality():
    pos1 = ChessPosition(3, 4)
    pos2 = ChessPosition(3, 4)
    pos3 = ChessPosition(4, 3)

    assert pos1 == pos2   # two positions with same row and col should be equal
    assert pos1 != pos3   # two positions with different row and col should not be equal

    # positions should work as dictionary keys
    # storing with pos1 and retrieving with pos2 should return same value
    # since pos1 and pos2 have same row and col
    pos_dict = {pos1: "test"}
    assert pos_dict[pos2] == "test"


