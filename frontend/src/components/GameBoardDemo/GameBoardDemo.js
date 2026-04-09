import React, { useState } from 'react';
import ChessBoard from '../ChessBoard';
import TicTacToeBoard from '../TicTacToeBoard';
import './GameBoardDemo.css';

/**
 * Demo page that showcases both game board components
 * with interactive sample data. Run `npm start` to preview.
 */
function GameBoardDemo() {
  const [activeTab, setActiveTab] = useState('tictactoe');

  // --- Tic-Tac-Toe demo state ---
  const [tttBoard, setTttBoard] = useState(Array(9).fill(null));
  const [tttPlayer, setTttPlayer] = useState('X');
  const [tttWinner, setTttWinner] = useState(null);

  const checkTttWinner = (board) => {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6],
    ];
    for (const [a, b, c] of lines) {
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return { winner: board[a], cells: [a, b, c] };
      }
    }
    return null;
  };

  const handleTttClick = (index) => {
    if (tttBoard[index] || tttWinner) return;
    const newBoard = [...tttBoard];
    newBoard[index] = tttPlayer;
    setTttBoard(newBoard);
    const result = checkTttWinner(newBoard);
    if (result) {
      setTttWinner(result);
    } else {
      setTttPlayer(tttPlayer === 'X' ? 'O' : 'X');
    }
  };

  const resetTtt = () => {
    setTttBoard(Array(9).fill(null));
    setTttPlayer('X');
    setTttWinner(null);
  };

  // --- Chess demo state ---
  const [chessSelected, setChessSelected] = useState(null);

  const handleChessClick = (row, col) => {
    if (chessSelected && chessSelected.row === row && chessSelected.col === col) {
      setChessSelected(null);
    } else {
      setChessSelected({ row, col });
    }
  };

  return (
    <div className="demo">
      <h1 className="demo-title">Game Board Components</h1>
      <p className="demo-subtitle">
        Interactive preview of the Chess and Tic-Tac-Toe UI components.
        These are visual shells only — no game engine is included.
      </p>

      <div className="demo-tabs">
        <button
          className={`demo-tab ${activeTab === 'tictactoe' ? 'demo-tab--active' : ''}`}
          onClick={() => setActiveTab('tictactoe')}
        >
          Tic-Tac-Toe
        </button>
        <button
          className={`demo-tab ${activeTab === 'chess' ? 'demo-tab--active' : ''}`}
          onClick={() => setActiveTab('chess')}
        >
          Chess
        </button>
      </div>

      {activeTab === 'tictactoe' && (
        <div className="demo-board-section">
          <TicTacToeBoard
            board={tttBoard}
            winningCells={tttWinner?.cells}
            currentPlayer={tttPlayer}
            isMyTurn={true}
            onCellClick={handleTttClick}
            playerSymbol="X"
            opponentName="Demo Opponent"
          />
          <button className="demo-reset" onClick={resetTtt}>
            Reset Board
          </button>
        </div>
      )}

      {activeTab === 'chess' && (
        <div className="demo-board-section">
          <ChessBoard
            currentPlayer="white"
            isMyTurn={true}
            onSquareClick={handleChessClick}
            selectedSquare={chessSelected}
            playerColor="white"
            opponentName="Demo Opponent"
          />
          <button className="demo-reset" onClick={() => setChessSelected(null)}>
            Clear Selection
          </button>
        </div>
      )}
    </div>
  );
}

export default GameBoardDemo;
