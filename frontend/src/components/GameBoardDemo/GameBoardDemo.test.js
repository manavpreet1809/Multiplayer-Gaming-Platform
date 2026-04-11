import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameBoardDemo from './GameBoardDemo';

jest.mock('../ChessBoard', () => (props) => (
  <div data-testid="chess-board">
    <div>Chess Mock</div>
    <button onClick={() => props.onSquareClick(0, 0)}>Select Chess Square</button>
    <div data-testid="selected-square">
      {props.selectedSquare ? `${props.selectedSquare.row},${props.selectedSquare.col}` : 'none'}
    </div>
  </div>
));

jest.mock('../TicTacToeBoard', () => (props) => (
  <div data-testid="ttt-board">
    <div>TicTacToe Mock</div>
    <button onClick={() => props.onCellClick(0)}>Play Cell 0</button>
    <button onClick={() => props.onCellClick(1)}>Play Cell 1</button>
    <button onClick={() => props.onCellClick(2)}>Play Cell 2</button>
    <div data-testid="current-player">{props.currentPlayer}</div>
    <div data-testid="winning-cells">
      {props.winningCells ? props.winningCells.join(',') : 'none'}
    </div>
  </div>
));

describe('GameBoardDemo', () => {
  test('renders title, subtitle, and Tic-Tac-Toe tab by default', () => {
    render(<GameBoardDemo />);

    expect(screen.getByText('Game Board Components')).toBeInTheDocument();
    expect(screen.getByText(/Interactive preview of the Chess and Tic-Tac-Toe UI components/i)).toBeInTheDocument();
    expect(screen.getByTestId('ttt-board')).toBeInTheDocument();
    expect(screen.queryByTestId('chess-board')).not.toBeInTheDocument();
  });

  test('switches to Chess tab when clicked', () => {
    render(<GameBoardDemo />);

    fireEvent.click(screen.getByText('Chess'));

    expect(screen.getByTestId('chess-board')).toBeInTheDocument();
    expect(screen.queryByTestId('ttt-board')).not.toBeInTheDocument();
  });

  test('updates Tic-Tac-Toe current player after a move', () => {
    render(<GameBoardDemo />);

    expect(screen.getByTestId('current-player')).toHaveTextContent('X');

    fireEvent.click(screen.getByText('Play Cell 0'));

    expect(screen.getByTestId('current-player')).toHaveTextContent('O');
  });

  test('resets Tic-Tac-Toe board state when reset button is clicked', () => {
    render(<GameBoardDemo />);

    fireEvent.click(screen.getByText('Play Cell 0'));
    expect(screen.getByTestId('current-player')).toHaveTextContent('O');

    fireEvent.click(screen.getByText('Reset Board'));

    expect(screen.getByTestId('current-player')).toHaveTextContent('X');
    expect(screen.getByTestId('winning-cells')).toHaveTextContent('none');
  });

  test('clears selected chess square when clear selection is clicked', () => {
    render(<GameBoardDemo />);

    fireEvent.click(screen.getByText('Chess'));
    fireEvent.click(screen.getByText('Select Chess Square'));

    expect(screen.getByTestId('selected-square')).toHaveTextContent('0,0');

    fireEvent.click(screen.getByText('Clear Selection'));

    expect(screen.getByTestId('selected-square')).toHaveTextContent('none');
  });
});