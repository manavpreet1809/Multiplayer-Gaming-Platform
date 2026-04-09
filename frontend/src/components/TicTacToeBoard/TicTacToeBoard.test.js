import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TicTacToeBoard from './TicTacToeBoard';

describe('TicTacToeBoard', () => {
  test('renders and handles cell click', () => {
    const onCell = jest.fn();
    render(
      <TicTacToeBoard
        board={Array(9).fill(null)}
        currentPlayer="X"
        isMyTurn
        onCellClick={onCell}
        playerSymbol="X"
        opponentName="Bob"
      />,
    );
    expect(screen.getByText(/your turn/i)).toBeInTheDocument();
    const cells = screen.getAllByRole('button');
    fireEvent.click(cells[0]);
    expect(onCell).toHaveBeenCalledWith(0);
  });
});
