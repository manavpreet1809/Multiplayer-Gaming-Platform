# Test Suite README

## Chess & TicTacToe — Unit Tests

This project contains unit tests for two game engines: Chess and TicTacToe.

- The tests are split across four files — two for each game — covering models (initial setup and structures) and engine logic (rules, move validation, and game flow).
- All tests are written using pytest and follow a consistent structure: set up a board state, perform an action, and assert the expected outcome.
- Tests cover initial state setup, valid and invalid moves, special rules, win/draw detection, and data integrity across board operations.

---

## Install pytest

Before running any tests, install pytest using the following command:

```bash
py -m pip install pytest
```
---


## Run All Tests at Once

To run all four test files together, navigate to the project root directory `seng300-202601-pg-3` and run:

```bash
py -m pytest src/app/tests/ -v
```
---

## Test Files

### 1. `test_chess_models.py`

**Run this file in root directory `seng300-202601-pg-3`  :**
```bash
py -m pytest src/app/tests/test_chess_models.py -v -s
```

**What is tested:**

- All pieces (pawns, rooks, knights, bishops, queens, kings) are placed in correct squares for both colors (white and black), and rows 2–5 are empty at setup.
- White pieces stay on rows 0–1, black pieces stay on rows 6–7
- `ChessPosition` stores row and column correctly, raises `ValueError` for out-of-range values, and supports equality and hashing for use as dictionary keys.
- `ChessMove` stores `fromPos`, `toPos`, and promotion correctly — no promotion defaults to `None`, and different promotion types (queen, rook, knight, bishop) are stored and compared correctly.
- `setPiece`, `removePiece`, and `getPiece` work correctly — placing stores the piece, removing leaves `None`, and replacing reflects the new piece.
- Cloning a board creates a fully independent copy — removing or modifying a piece in the clone does not affect the original board.
- Pieces return correct single-character codes (uppercase for white, lowercase for black), and `toList()` produces the correct 8×8 grid for both the starting position and a mid-game state.


---

### 2. `test_chess_engine.py`

**Run this file in root directory `seng300-202601-pg-3`:**
```bash
py -m pytest src/app/tests/test_chess_engine.py -v -s
```

**What is tested:**

- White moves first, players are assigned to colors, en passant target starts as `None`, halfmove clock starts at `0`, and all four castling rights are `True` at game start.
- Moving from an empty square, moving the wrong color, moving to the same square, and capturing your own piece are all correctly rejected.
- Pawns can move one or two squares forward from the start row, cannot move backward, can capture diagonally, and cannot move into an occupied square directly ahead.
- Rooks move horizontally and vertically but are blocked by pieces and cannot move diagonally
- bishops move diagonally only.
- knights move in L-shapes and can jump over pieces.
- Queens move in all directions and are blocked by pieces after initial setup.
- kings move one square in any direction, cannot move two squares, and cannot move into a square attacked by the opponent.
- Kingside and queenside castling are valid when the path is clear, blocked when pieces are in the way, and castling rights are revoked after the king moves.
- En passant target is set correctly after a pawn double-move, and en passant capture is validated; pawn promotion defaults to queen and can also promote to rook when specified.
- Turns switch after each move, halfmove clock increments on non-pawn/non-capture moves and resets on pawn moves, captured pieces are removed, and `hasMoved` is set after a piece moves.
- `evaluateEnd` correctly detects checkmate (win for opponent), stalemate (draw), and the 50-move rule (draw when halfmove clock reaches 100).

---

### 3. `test_tictactoe_models.py`

**Run this file in root directory `seng300-202601-pg-3`:**
```bash
py -m pytest src/app/tests/test_tictactoe_models.py -v -s
```

**What is tested:**

- `TicTacToePosition` stores row and column correctly, positions with different rows or columns are not equal, and equal positions share the same hash value.
- Positions can be used interchangeably as dictionary keys when they have the same row and column values.
- All nine cells start as `None` on a new board, and `isFull()` returns `False` for an empty board.
- `setCell` stores `"X"` and `"O"` correctly at any position, and different cells are fully independent of each other.
- `isFull()` returns `True` when all nine cells are filled and `False` when even one cell remains empty.
- `Player.X` has value `"X"`, `Player.O` has value `"O"`, they are not equal, and there are exactly two players in the enum.
- `toList()` returns a flat 9-element list with `None` for empty cells and the correct player mark for filled cells.

---

### 4. `test_tictactoe_engine.py`

**Run this file in root directory `seng300-202601-pg-3`:**
```bash
py -m pytest src/app/tests/test_tictactoe_engine.py -v -s
```

**What is tested:**

- The first player is set as active at the start, the move counter starts at `0`, and both players are assigned correctly.
- Placing on an empty cell is valid; placing on an occupied cell, out-of-bounds position, or negative index is rejected; all four corners are valid on an empty board.
- After a move, the correct player's mark appears on the chosen cell, the current player switches, and the move counter increments by one.
- The player switches back to the first player after two moves, and applying a move always reflects the mark in the returned state.
- Wins are detected correctly for all eight lines — top row, middle row, left column, right column, main diagonal, and anti-diagonal — with the correct winner returned each time.
- A full board with no winner correctly returns a draw, and `evaluateEnd` returns `None` at the start and during an ongoing mid-game.
- `serializeState` maps player names to `"X"`/`"O"` symbols correctly, and `deserializeMove` converts a flat index (0–8) into the correct row and column.


