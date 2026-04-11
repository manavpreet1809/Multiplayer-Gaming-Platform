import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameLobby from './GameLobby';

describe('GameLobby', () => {
  const mockLeave = jest.fn();
  const mockToggleReady = jest.fn();
  const mockStartGame = jest.fn();

  const players = [
    { id: 1, username: 'Alice', isReady: true },
    { id: 2, username: 'Bob', isReady: false },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders lobby title, id, and waiting status', () => {
    render(
      <GameLobby
        lobbyId="12345"
        gameName="Chess"
        status="waiting"
        players={players}
      />
    );

    expect(screen.getByText('Chess Lobby')).toBeInTheDocument();
    expect(screen.getByText('Lobby ID: 12345')).toBeInTheDocument();
    expect(screen.getByText('Waiting for players')).toBeInTheDocument();
  });

  test('renders players and empty waiting slots correctly', () => {
    render(
      <GameLobby
        lobbyId="12345"
        gameName="Chess"
        players={[players[0]]}
        requiredPlayers={2}
      />
    );

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Ready')).toBeInTheDocument();
    expect(screen.getByText('Waiting for player…')).toBeInTheDocument();
  });

  test('calls onLeaveLobby when leave button is clicked', () => {
    render(
      <GameLobby
        lobbyId="12345"
        gameName="Chess"
        players={players}
        onLeaveLobby={mockLeave}
      />
    );

    fireEvent.click(screen.getByText('Leave Lobby'));
    expect(mockLeave).toHaveBeenCalled();
  });

  test('calls onToggleReady when toggle ready button is clicked', () => {
    render(
      <GameLobby
        lobbyId="12345"
        gameName="Chess"
        status="waiting"
        players={players}
        onToggleReady={mockToggleReady}
      />
    );

    fireEvent.click(screen.getByText('Toggle Ready'));
    expect(mockToggleReady).toHaveBeenCalled();
  });

  test('shows start game button only when enough players are present and calls onStartGame', () => {
    render(
      <GameLobby
        lobbyId="12345"
        gameName="Chess"
        status="waiting"
        players={players}
        requiredPlayers={2}
        onStartGame={mockStartGame}
      />
    );

    const startButton = screen.getByText('Start Game');
    expect(startButton).toBeInTheDocument();

    fireEvent.click(startButton);
    expect(mockStartGame).toHaveBeenCalled();
  });
});