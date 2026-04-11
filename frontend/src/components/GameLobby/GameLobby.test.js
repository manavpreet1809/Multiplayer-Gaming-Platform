import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GameLobby from './GameLobby';

describe('GameLobby', () => {
  test('renders lobby and players', () => {
    const onLeave = jest.fn();
    render(
      <GameLobby
        lobbyId="ABCD"
        gameName="Chess"
        status="waiting"
        players={[{ id: 'a', username: 'a', isReady: false }]}
        requiredPlayers={2}
        onLeaveLobby={onLeave}
      />,
    );
    expect(screen.getByText(/chess lobby/i)).toBeInTheDocument();
    expect(screen.getByText(/ABCD/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /leave lobby/i }));
    expect(onLeave).toHaveBeenCalled();
  });

  test('shows start when host can start', () => {
    const onStart = jest.fn();
    render(
      <GameLobby
        lobbyId="X"
        gameName="Chess"
        status="waiting"
        players={[
          { id: 'a', username: 'a', isReady: true },
          { id: 'b', username: 'b', isReady: true },
        ]}
        requiredPlayers={2}
        onStartGame={onStart}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /start game/i }));
    expect(onStart).toHaveBeenCalled();
  });
});
