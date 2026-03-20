# Chess Engine Validation Pipeline

## 1. Overview

Chess is a two-player strategy game utilizing an 8x8 game board. Each player is assigned a colour (Color.WHITE or Color.BLACK) and each colour has 16 available pieces with varying types (PieceType.PAWN, PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN, and PieceType.KING)

The goal of the game for either player is to reach a checkmate using valid moves of each piece, which only happens when the next turn on either player's side results in an inevitable valid move that can capture a king. Otherwise, a stalemate or draw is reached through either an impossibility of a checkmate or once the 50 move draw rule has passed as the game progresses.

Rules and Validation is in charge of the validation pipeline that ensures pass-through of valid moves, rejection of invalid moves, and update of the game state.

## 2. Game Engine Architecture

chessEngine inherits from the abstract base class (similar to a Java interface) gameEngine in gameEngine.py (found under modules) used for both our project's games, chess and tic-tac-toe.

gameEngine has four abstract methods that chessEngine implements:
1. createInitialState() - sets up the initial chess board and starting game state
2. validateMove() - ensures that the requested player move is valid
3. applyMove() - updates the game state once a move has been validated
4. evaluateEnd() - checks if the game has ended and returns the result

## 3. Validation Pipeline

## 4. Validation Rules

## 5. Supported Features

In terms of general game logic, the chess engine fully supports all rules that typically appear in any standard chess game.

These include:
- pawn promotion
- en passant
- king-side castling
- queen-side castling
- 50 move draw rule