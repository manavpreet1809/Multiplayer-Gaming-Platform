# Chess Engine Validation Pipeline

## 1. Overview

Chess is a two-player strategy game utilizing an 8x8 game board. Each player is assigned a colour (Color.WHITE or Color.BLACK) and each colour has 16 available pieces with varying types (PieceType.KING, PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT, and PieceType.PAWN).

The goal of the game for either player is to reach a checkmate using valid moves of each piece, which only occurs when a king is in check and can't escape from the threat. Otherwise, a stalemate or draw is reached through either an impossibility of a checkmate or once the 50-move draw rule has passed throughout game progression.

Rules and Validation is in charge of the validation pipeline that ensures the pass-through of valid moves, rejection of invalid moves, and updates to the game state.

## 2. Game Engine Architecture

ChessEngine inherits from the abstract base class (similar to a Java interface) GameEngine in gameEngine.py (found under modules) used for both our project's games, chess and tic-tac-toe.

GameEngine has four abstract methods that ChessEngine implements:
1. createInitialState() - sets up the initial chess board and starting game state
2. validateMove() - ensures that the requested player move is valid
3. applyMove() - updates the game state once a move has been validated
4. evaluateEnd() - checks if the game has ended and returns the result

## 3. Validation Pipeline

The following implementation of these methods in ChessEngine handle the majority of our validation:

- validateMove()
- applyMove()
- evaluateEnd()

When a player submits a move, the engine follows ordered steps to ensure the move is legal and updates the game state:

### validateMove() -> bool

The engine first gets the following information:
- The state of the board (state["board"])
- The current selected piece (fromPos)
- The target square (toPos)

Then it checks the following:

1. Is there a piece at the source square? - Move is rejected if fromPos does not contain a piece
2. Does the piece belong to the active player? - Move is rejected if the piece's colour doesn't match state["activeColor"]
3. Is the target square valid? - Move is rejected if fromPos is equal to toPos
4. Can the target piece be taken? - Move is rejected if target piece is the same as the current player's colour
5. Can the current piece actually apply the move? - These implementations are abstracted within the isLegalMove() helper method, but are applicable to all piece types. Move is rejected accordingly to the rules of the corresponding piece type:
- PieceType.KING: 1 move in any direction
- PieceType.QUEEN: diagonal or horizontal moves
- PieceType.ROOK: horizontal moves only
- PieceType.BISHOP: diagonal moves only
- PieceType.KNIGHT: L-shape moves only
- PieceType.PAWN: 1 or 2 moves forward if never moved, 1 move forward only otherwise
6. Would this move leave the king in check? - Also abstracted within the wouldLeaveKingInCheck() helper method, however the general idea is that if the opponent can immediately capture the king on the next move, it is considered invalid and must be rejected.

Otherwise, if all validation steps pass, the method accepts the move and returns True.

**Note**: validateMove() does not actually verify the identity of the player making the move. Turn enforcement (mapping player ID to colour) is expected to be handled externally outside ChessEngine.

### applyMove() -> dict

(WIP)

### evaluateEnd() -> Optional[dict]

(WIP)

## 4. Validation Rules

The validation pipeline ensures that the following are properly applied:
1. Enforcement of turns - Only the current player should be able to move their pieces
2. Legality of moves - Each piece moves according to its piece type and its specific move rules
3. King safety - Moves that would put the king in check are rejected
4. Board constraints - Moves off the board and capturing pieces of the same colour are rejected
5. Game end detection - Checkmate, stalemate, and draws are enforced

## 5. Supported Features

In terms of general game logic, the chess engine fully supports all rules that typically appear in any standard chess game.

These include:
- White always goes first
- Pawn promotion
- En passant
- King-side castling
- Queen-side castling
- 50-move draw rule