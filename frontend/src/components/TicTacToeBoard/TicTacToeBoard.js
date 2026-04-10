import React from 'react';
import './TicTacToeBoard.css';

/**
 * TicTacToeBoard – visual board component (UC-13 UI).
 *
 * Props:
 *   board              – flat array of 9 values: "X" | "O" | null
 *   winningCells       – array of indices that form the winning line (e.g. [0,1,2]), or null
 *   currentPlayer      – "X" | "O" (whose turn it is)
 *   isMyTurn           – whether the local player can interact
 *   onCellClick(index) – called when a cell is clicked
 *   playerSymbol       – "X" | "O" – the local player's symbol
 *   opponentName       – display name of the opponent
 */
function TicTacToeBoard({
  board = Array(9).fill(null),
  winningCells,
  currentPlayer,
  isMyTurn = false,
  onCellClick,
  playerSymbol,
  opponentName,
}) {
  const isWinningCell = (index) => winningCells && winningCells.includes(index);

  return (
    <div className="ttt">
      <div className="ttt-info">
        <div className="ttt-players">
          <span className={`ttt-player ${currentPlayer === playerSymbol ? 'ttt-player--active' : ''}`}>
            You ({playerSymbol})
          </span>
          <span className="ttt-vs">vs</span>
          <span className={`ttt-player ${currentPlayer !== playerSymbol ? 'ttt-player--active' : ''}`}>
            {opponentName || 'Opponent'} ({playerSymbol === 'X' ? 'O' : 'X'})
          </span>
        </div>
        <p className="ttt-turn">
          {winningCells
            ? 'Game Over'
            : isMyTurn
              ? 'Your turn'
              : "Opponent's turn"}
        </p>
      </div>

      <div className="ttt-board" role="grid" aria-label="Tic-Tac-Toe board">
        {board.map((cell, index) => (
          <button
            key={index}
            className={`ttt-cell ${
              cell === 'X' ? 'ttt-cell--x' : cell === 'O' ? 'ttt-cell--o' : ''
            } ${isWinningCell(index) ? 'ttt-cell--winning' : ''}`}
            onClick={() => onCellClick && onCellClick(index)}
            disabled={!isMyTurn || cell !== null || !!winningCells}
            aria-label={`Row ${Math.floor(index / 3) + 1}, Column ${(index % 3) + 1}${cell ? `, ${cell}` : ', empty'}`}
          >
            {cell && <span className="ttt-mark">{cell}</span>}
          </button>
        ))}
      </div>
    </div>
  );
}

export default TicTacToeBoard;
