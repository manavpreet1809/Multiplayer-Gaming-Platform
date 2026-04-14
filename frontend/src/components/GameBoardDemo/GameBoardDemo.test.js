import React from 'react';
import { render, screen } from '@testing-library/react';
import GameBoardDemo from './GameBoardDemo';

describe('GameBoardDemo', () => {
  test('renders demo tabs', () => {
    render(<GameBoardDemo />);
    expect(screen.getByRole('button', { name: /tic-tac-toe/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /chess/i })).toBeInTheDocument();
  });
});
