# TicTacToe Engine Validation Pipeline

## 1. Overview

Tic-tac-toe is a two-player strategy game played on a 3x3 game board. Each player is assigned a unique mark (X or O) that they can place down on each square of the board.

The goal of the game for either player is to align three of their marks in a row, either vertically, horizontally, or diagonally. Otherwise, a draw is reached when the board is completely filled with marks but this winning condition has not yet been met.

Rules and Validation are in charge of the validation pipeline that ensures the pass-through of valid moves, rejection of invalid moves, and updates to the game state.

## 2. Game Engine Architecture

TicTacToeEngine inherits from the abstract base class (similar to a Java interface) GameEngine in gameEngine.py (found under modules) used for both our project's games, chess and tic-tac-toe.

GameEngine has four abstract methods that TicTacToeEngine implements:
1. createInitialState() - sets up the initial tic-tac-toe board and starting game state
2. validateMove() - ensures that the requested player move is valid
3. applyMove() - updates the game state once a move has been validated
4. evaluateEnd() - checks if the game has ended and returns the result

## 3. Validation Pipeline

The following implementation of these methods in TicTacToeEngine handle the majority of our validation:

- validateMove()
- applyMove()
- evaluateEnd()

When a player submits a move, the engine follows ordered steps to ensure the move is legal and updates the game state:

### validateMove() -> bool

validateMove() checks the following:

1. Is the target position within the bounds? - Move is rejected if target position is out of bounds of the 3x3 board
2. Is the target position empty? - Move is rejected if the target position already contains a mark

Otherwise, if all validation steps pass, the method accepts the move and returns True.

**Note**: validateMove() does not verify the identity of the player making the move. Turn enforcement is handled externally through state["currentPlayer"].

### applyMove() -> dict

After a move has been validated, applyMove() updates the game state in the following way: 

1. First, it makes a clone of the tic-tac-toe board so that the original board is not directly mutated
2. Then, it applies the move to that cloned board

applyMove() then returns the game state in the form of a dictionary, including the cloned board with the applied move, player states, the new current player, and number of moves incremented. 

### evaluateEnd() -> Optional[dict]

After a move is applied, evaluateEnd() determines whether the game has ended and returns the result.

evaluateEnd() checks the following in order:

1. Rows
2. Columns
3. Diagonals

At any point, if three marks of the same type appear in any of these orientations, the game results in a win. evaluateEnd() returns game state over, result as a win, and winner through one of the positions in the winning orientation as a dictionary.

4. Draw

At this point, evaluateEnd() simply needs to check if the number of moves made is 9 (state["moves"] == 9) as it has already previously evaluated that no draw has been made by above. evaluateEnd() returns game state over and result as draw as a dictionary.

Otherwise, if none of the events above happen, the game simply continues and evaluateEnd() returns None.

## 4. Validation Rules

The validation pipeline ensures that the following are properly applied:
1. Legality of moves - Marks must not overlap with existing marks already placed, and each player must place one mark per turn
2. Enforcement of turns - Only the current player should be able to place their mark.
3. Board constraints - Moves off the board are rejected
4. Game end detection - Win and draw conditions are enforced

## 5. Supported Features

In terms of general game logic, the tic-tac-toe engine fully supports all necessary rules that appear in any standard tic-tac-toe game.

These include:
- Each player only places one mark type (X or O)
- Marks must not overlap
- Game ends in a win if three marks in a row are detected
- Game ends in a draw if all nine positions are full and win condition not met