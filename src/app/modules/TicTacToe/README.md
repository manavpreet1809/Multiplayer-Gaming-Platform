# TicTacToe Engine Validation Pipeline

## 1. Overview

Tic-tac-toe is a two-player strategy game played on a 3x3 game board. Each player is assigned a unique mark (X or O) that they can place down on each square of the board.

The goal of the game for either player is to align their marks three marks in a row, either vertically, horizontally, or diagonally. Otherwise, a draw is reached when the board is completely filled with marks but this winning condition has not been met yet.

Rules and Validation are in charge of the validation pipeline that ensures the pass-through of valid moves, rejection of invalid moves, and updates to the game state.

## 2. Game Engine Architecture

TicTacToeEngine inherits from the abstract base class (similar to a Java interface) GameEngine in gameEngine.py (found under modules) used for both our project's games, chess and tic-tac-toe.

GameEngine has four abstract methods that ChessEngine implements:
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

### applyMove() -> dict

### evaluateEnd() -> Optional[dict]

## 4. Validation Rules

The validation pipeline ensures that the following are properly applied:

## 5. Supported Features

