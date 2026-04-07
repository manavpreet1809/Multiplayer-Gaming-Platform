import React, { useMemo } from 'react';
import './ChessBoard.css';

/**
 * Unicode symbols for chess pieces.
 * White pieces: King ♔ Queen ♕ Rook ♖ Bishop ♗ Knight ♘ Pawn ♙
 * Black pieces: King ♚ Queen ♛ Rook ♜ Bishop ♝ Knight ♞ Pawn ♟
 */
const PIECE_SYMBOLS = {
  K: '\u2654', Q: '\u2655', R: '\u2656', B: '\u2657', N: '\u2658', P: '\u2659',
  k: '\u265A', q: '\u265B', r: '\u265C', b: '\u265D', n: '\u265E', p: '\u265F',
};

const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
const RANKS = [8, 7, 6, 5, 4, 3, 2, 1];

/**
 * ChessBoard – visual board component (UC-13 UI).
 *
 * Props:
 *   board              – 8x8 array of piece codes (e.g. "K","p") or null for empty.
 *                         board[row][col], row 0 = rank 8 (black's back rank).
 *   selectedSquare     – { row, col } of the currently selected square, or null
 *   highlightedSquares – array of { row, col } for legal-move indicators
 *   lastMove           – { from: {row,col}, to: {row,col} } to highlight the last move
 *   currentPlayer      – "white" | "black"
 *   isMyTurn           – whether the local player can interact
 *   onSquareClick(row, col) – called when a square is clicked
 *   playerColor        – "white" | "black" – the local player's color
 *   opponentName       – display name of the opponent
 *   capturedByWhite    – array of piece codes captured by white
 *   capturedByBlack    – array of piece codes captured by black
 */
function ChessBoard({
  board,
  selectedSquare,
  highlightedSquares = [],
  lastMove,
  currentPlayer,
  isMyTurn = false,
  onSquareClick,
  playerColor = 'white',
  opponentName,
  capturedByWhite = [],
  capturedByBlack = [],
}) {
  const isLight = (row, col) => (row + col) % 2 === 0;

  const isSelected = (row, col) =>
    selectedSquare && selectedSquare.row === row && selectedSquare.col === col;

  const isHighlighted = (row, col) =>
    highlightedSquares.some((sq) => sq.row === row && sq.col === col);

  const isLastMove = (row, col) =>
    lastMove &&
    ((lastMove.from.row === row && lastMove.from.col === col) ||
      (lastMove.to.row === row && lastMove.to.col === col));

  const isWhitePiece = (piece) => piece && piece === piece.toUpperCase();

  // Flip board if playing black (memoized — only recomputes when playerColor changes)
  const { displayRows, displayCols, rowIndices, colIndices } = useMemo(() => {
    const flipped = playerColor === 'black';
    const seq = [0, 1, 2, 3, 4, 5, 6, 7];
    const rev = [7, 6, 5, 4, 3, 2, 1, 0];
    return {
      displayRows: flipped ? [...RANKS].reverse() : RANKS,
      displayCols: flipped ? [...FILES].reverse() : FILES,
      rowIndices: flipped ? rev : seq,
      colIndices: flipped ? rev : seq,
    };
  }, [playerColor]);

  // Default starting position if no board prop provided
  const defaultBoard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
  ];

  const currentBoard = board || defaultBoard;

  return (
    <div className="chess">
      <div className="chess-info">
        <div className="chess-players">
          <span className={`chess-player ${currentPlayer === playerColor ? 'chess-player--active' : ''}`}>
            You ({playerColor})
          </span>
          <span className="chess-vs">vs</span>
          <span className={`chess-player ${currentPlayer !== playerColor ? 'chess-player--active' : ''}`}>
            {opponentName || 'Opponent'} ({playerColor === 'white' ? 'black' : 'white'})
          </span>
        </div>
        <p className="chess-turn">
          {isMyTurn ? 'Your turn' : "Opponent's turn"}
        </p>
      </div>

      <div className="chess-captured chess-captured--opponent">
        {(playerColor === 'white' ? capturedByBlack : capturedByWhite).map((piece, i) => (
          <span key={i} className="chess-captured-piece">
            {PIECE_SYMBOLS[piece]}
          </span>
        ))}
      </div>

      <div className="chess-board-wrapper">
        {/* Rank labels (left side) */}
        <div className="chess-rank-labels">
          {rowIndices.map((ri) => (
            <span key={ri} className="chess-label">{displayRows[playerColor === 'black' ? 7 - ri : ri]}</span>
          ))}
        </div>

        <div className="chess-board" role="grid" aria-label="Chess board">
          {rowIndices.map((ri) =>
            colIndices.map((ci) => {
              const piece = currentBoard[ri][ci];
              return (
                <button
                  key={`${ri}-${ci}`}
                  className={[
                    'chess-square',
                    isLight(ri, ci) ? 'chess-square--light' : 'chess-square--dark',
                    isSelected(ri, ci) ? 'chess-square--selected' : '',
                    isHighlighted(ri, ci) ? 'chess-square--highlighted' : '',
                    isLastMove(ri, ci) ? 'chess-square--last-move' : '',
                  ]
                    .filter(Boolean)
                    .join(' ')}
                  onClick={() => onSquareClick && onSquareClick(ri, ci)}
                  disabled={!isMyTurn && !selectedSquare}
                  aria-label={`${displayCols[playerColor === 'black' ? 7 - ci : ci]}${displayRows[playerColor === 'black' ? 7 - ri : ri]}${piece ? `, ${isWhitePiece(piece) ? 'white' : 'black'} ${piece.toLowerCase()}` : ''}`}
                >
                  {piece && (
                    <span className={`chess-piece ${isWhitePiece(piece) ? 'chess-piece--white' : 'chess-piece--black'}`}>
                      {PIECE_SYMBOLS[piece]}
                    </span>
                  )}
                  {isHighlighted(ri, ci) && !piece && (
                    <span className="chess-move-dot" />
                  )}
                  {isHighlighted(ri, ci) && piece && (
                    <span className="chess-capture-ring" />
                  )}
                </button>
              );
            })
          )}
        </div>

        {/* File labels (bottom) */}
        <div className="chess-file-labels">
          <span className="chess-label-spacer" />
          {colIndices.map((ci) => (
            <span key={ci} className="chess-label">{displayCols[playerColor === 'black' ? 7 - ci : ci]}</span>
          ))}
        </div>
      </div>

      <div className="chess-captured chess-captured--player">
        {(playerColor === 'white' ? capturedByWhite : capturedByBlack).map((piece, i) => (
          <span key={i} className="chess-captured-piece">
            {PIECE_SYMBOLS[piece]}
          </span>
        ))}
      </div>
    </div>
  );
}

export default ChessBoard;
