import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameList from './GameList';

const games = [
  { id: 'chess', name: 'Chess', description: 'Classic', playerCount: 2 },
];

describe('GameList', () => {
  test('empty state', () => {
    render(<GameList games={[]} />);
    expect(screen.getByText(/no games available/i)).toBeInTheDocument();
  });

  test('select game notifies callback', () => {
    const onSelect = jest.fn();
    render(
      <GameList games={games} selectedGameId={null} onSelectGame={onSelect} onJoinLobby={jest.fn()} />,
    );
    fireEvent.click(screen.getByRole('button', { name: /chess/i }));
    expect(onSelect).toHaveBeenCalledWith('chess');
  });

  test('join lobby uses selected game', () => {
    const onJoin = jest.fn();
    render(
      <GameList games={games} selectedGameId="chess" onSelectGame={jest.fn()} onJoinLobby={onJoin} />,
    );
    fireEvent.click(screen.getByRole('button', { name: /join lobby/i }));
    expect(onJoin).toHaveBeenCalledWith('chess');
  });
});
