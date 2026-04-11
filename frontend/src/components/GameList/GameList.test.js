import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameList from './GameList';

describe('GameList', () => {
  const mockSelect = jest.fn();
  const mockJoin = jest.fn();
  const mockBack = jest.fn();

  const games = [
    { id: 'chess', name: 'Chess', description: 'Strategy game', playerCount: 2 },
    { id: 'ttt', name: 'TicTacToe', description: 'Simple game', playerCount: 2 },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders empty message when no games are available', () => {
    render(<GameList games={[]} />);

    expect(screen.getByText('No games available at this time.')).toBeInTheDocument();
  });

  test('renders list of games', () => {
    render(<GameList games={games} />);

    expect(screen.getByText('Chess')).toBeInTheDocument();
    expect(screen.getByText('TicTacToe')).toBeInTheDocument();
  });

  test('calls onSelectGame when a game is clicked', () => {
    render(<GameList games={games} onSelectGame={mockSelect} />);

    fireEvent.click(screen.getByText('Chess'));

    expect(mockSelect).toHaveBeenCalledWith('chess');
  });

  test('shows selected game details and allows joining lobby', () => {
    render(
      <GameList
        games={games}
        selectedGameId="chess"
        onJoinLobby={mockJoin}
      />
    );

    expect(screen.getByText('Strategy game')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Join Lobby'));

    expect(mockJoin).toHaveBeenCalledWith('chess');
  });

  test('calls onBack when back button is clicked', () => {
    render(<GameList games={games} onBack={mockBack} />);

    fireEvent.click(screen.getByText('Back'));

    expect(mockBack).toHaveBeenCalled();
  });
});