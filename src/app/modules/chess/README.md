# Chess Engine Validation Pipeline

## 1. Overview

Chess is a two-player strategy game utilizing an 8x8 game board. Each player is assigned a colour (Color.WHITE or Color.BLACK) and each colour has 16 available pieces with varying types (PieceType.PAWN, PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN, and PieceType.KING)

The goal of the game for either player is to reach a checkmate using valid moves of each piece, which only happens when the next turn on either player's side results in an inevitable valid move that can capture a king. Otherwise, a stalemate or draw is reached through either an impossitibility of a checkmate or once the 50-move draw rule has passed.

Rules and Validation is in charge of the validation pipeline that ensures the pass-through of valid moves, rejection of invalid moves, and update of the game state.

## 2. Game Engine Architecture

## 3. Validation Pipeline

## 4. Validation Rules

## 5. Supported Features
