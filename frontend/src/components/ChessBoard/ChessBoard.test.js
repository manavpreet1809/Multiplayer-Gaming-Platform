import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ChessBoard from './ChessBoard';

describe('ChessBoard', () => {
  const mockClick = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders default chess board with 64 squares', () => {
    render(<ChessBoard onSquareClick={mockClick} />);

    const squares = screen.getAllByRole('button');
    expect(squares.length).toBe(64);
  });

  test('calls onSquareClick when a square is clicked', () => {
    render(<ChessBoard onSquareClick={mockClick} isMyTurn={true} />);

    const squares = screen.getAllByRole('button');
    fireEvent.click(squares[0]);

    expect(mockClick).toHaveBeenCalled();
  });

  test('disables square clicks when not player turn and no selection', () => {
    render(<ChessBoard onSquareClick={mockClick} isMyTurn={false} />);

    const squares = screen.getAllByRole('button');

    expect(squares[0]).toBeDisabled();
  });

  test('renders player and opponent names correctly', () => {
    render(
      <ChessBoard
        playerColor="white"
        opponentName="John"
        currentPlayer="white"
      />
    );

    expect(screen.getByText('You (white)')).toBeInTheDocument();
    expect(screen.getByText('John (black)')).toBeInTheDocument();
  });

  test('renders captured pieces correctly', () => {
    render(
      <ChessBoard
        capturedByWhite={['p', 'q']}
        capturedByBlack={['P']}
        playerColor="white"
      />
    );

    const capturedPieces = screen.getAllByRole('img');
    expect(capturedPieces.length).toBeGreaterThan(0);
  });
});