import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameResults from './GameResults';

describe('GameResults', () => {
  test('win state', () => {
    const onDash = jest.fn();
    render(
      <GameResults
        result="win"
        winnerUsername="bob"
        mmrChange={25}
        newRank="Silver"
        onReturnDashboard={onDash}
      />,
    );
    expect(screen.getByText(/victory/i)).toBeInTheDocument();
    expect(screen.getByText(/bob/i)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /return to dashboard/i }));
    expect(onDash).toHaveBeenCalled();
  });

  test('draw state', () => {
    render(<GameResults result="draw" mmrChange={5} onPlayAgain={jest.fn()} />);
    expect(screen.getByRole('heading', { name: /draw/i })).toBeInTheDocument();
  });
});
