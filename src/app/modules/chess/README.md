# Chess Engine Validation Pipeline

## 1. Overview

Chess is a two-player strategy game utilizing an 8x8 game board. Each player is assigned a colour (white or black), and each colour has 16 available pieces with varying types (king, queen, rook, bishop, knight, and pawn).

The goal of the game for either player is to reach a checkmate using valid moves of each piece, which only occurs when a king is in check and can't escape from the threat. Otherwise, a stalemate or draw occurs either when a checkmate is impossible or once the 50-move draw rule has passed.

Rules and Validation are in charge of the validation pipeline that ensures the pass-through of valid moves, rejection of invalid moves, and updates to the game state.

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

validateMove() checks the following:

1. Is there a piece at the source square? - Move is rejected if source position does not contain a piece
2. Does the piece belong to the active player? - Move is rejected if the piece's colour doesn't match state["activeColor"]
3. Is the target square valid? - Move is rejected if source position is equal to target position
4. Can the target piece be taken? - Move is rejected if target piece is the same as the current player's colour
5. Can the current piece actually apply the move? - These implementations are abstracted within the isLegalMove() helper method, but are applicable to all piece types. Move is rejected accordingly to the rules of the corresponding piece type:
- King: 1 move in any direction
- Queen: horizontal, vertical, or diagonal moves
- Rook: horizontal or vertical moves only
- Bishop: diagonal moves only
- Knight: L-shape moves only
- Pawn: 1 or 2 moves forward if the pawn has not yet moved, 1 move forward only otherwise. It can also do diagonal captures and special rules (promotion and en passant, which are handled seperately)
6. Would this move leave the king in check? - Also abstracted within the wouldLeaveKingInCheck() helper method, however the general idea is that if the opponent can immediately capture the king on the next move, it is considered invalid and must be rejected.

Otherwise, if all validation steps pass, the method accepts the move and returns True.

**Note**: validateMove() does not actually verify the identity of the player making the move. Turn enforcement (mapping player ID to colour) is expected to be handled externally outside ChessEngine.

### applyMove() -> dict

After a move has been validated, applyMove() updates the game state accordingly based on several scenarios: 

1. Basic move - Simply moves a piece from the source position to the target position
2. Castling
- King-side (short) castling: Rook on the far-right is moved to the square next to the king
- Queen-side (long) castling: Rook on the far-left is moved to the square next to king
- Importantly, castling rights are revoked after either of these moves are applied
3. Pawn promotion - Promotes a pawn on the back of a rank to any chosen piece other than a pawn or king (default option is queen)
4. En passant
- En passant capture: If the move matches an en passant target, the captured pawn is removed from the board
- En passant target update: If a pawn moves two squares forward, the skipped square is marked as the new en passant target
5. Halfmove clock - Is reset to zero if a pawn was moved or a piece was captured. Otherwise, it is incremented

applyMove() then returns the game state in the form of a dictionary, including the board, player states, new active player's colour, castling rights, en passant target (if any), and the halfmove clock. Importantly, it also ensures that the original state is not directly mutated.

### evaluateEnd() -> Optional[dict]

After a move is applied, evaluateEnd() determines whether the game has ended and returns the result:

1. 50-move draw rule

If 100 halfmoves (50 moves per player) have passed without the capture or movement of a pawn, the game is declared a draw. evaluateEnd() returns game state over, result as draw, and reason by 50-move rule as a dictionary.

2. Checkmate

If the active player's king is currently under attack and does not have any legal moves, the game results in a checkmate. evaluateEnd() returns game state over, result as win, assigns the winning player, and reason by checkmate as a dictionary.

3. Stalemate

If the active player's king is not currently under attack and does not have any legal moves, the game results in a stalemate. evaluateEnd() returns game state over, result as draw, and reason by stalemate as a dictionary.

Otherwise, if none of the events above happen, the game simply continues and evaluateEnd() returns None.

## 4. Validation Rules

The validation pipeline ensures that the following are properly applied:
1. Legality of moves - Each piece moves according to its piece type and its specific move rules
2. Enforcement of turns - Only the current player should be able to move their pieces
3. King safety - Moves that would put the king in check are rejected
4. Board constraints - Moves off the board and capturing pieces of the same colour are rejected
5. Game end detection - Checkmate, stalemate, and draws are enforced

## 5. Supported Features

In terms of general game logic, the chess engine fully supports all necessary rules that appear in any standard chess game.

These include:
- White always going first
- Pawn promotion
- En passant
- King-side (short) castling
- Queen-side (long) castling
- 50-move draw rule