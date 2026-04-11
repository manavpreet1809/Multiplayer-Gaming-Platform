import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ChessBoard from './ChessBoard';

describe('ChessBoard', () => {
  test('renders grid and player labels', () => {
    const onClick = jest.fn();
    render(
      <ChessBoard
        currentPlayer="white"
        isMyTurn
        onSquareClick={onClick}
        playerColor="white"
        opponentName="Other"
      />,
    );
    expect(screen.getByRole('grid', { name: /chess board/i })).toBeInTheDocument();
    expect(screen.getByText(/you \(white\)/i)).toBeInTheDocument();
    const squares = screen.getAllByRole('button');
    expect(squares.length).toBeGreaterThanOrEqual(64);
    fireEvent.click(squares[0]);
    expect(onClick).toHaveBeenCalled();
  });
});
