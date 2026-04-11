import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import { Routes, Route } from 'react-router-dom';
import LobbyPage from './LobbyPage';
import { renderWithAuth } from '../../test/testUtils';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('LobbyPage', () => {
  beforeEach(() => {
    gameService.getGame.mockResolvedValue({
      game_id: 'g1',
      lobby_code: 'ZZZZ',
      game_type: 'chess',
      status: 0,
      host_id: 'tester',
      player_ids: ['tester'],
      max_players: 2,
    });
    gameService.createGameWebSocket.mockImplementation(async (_id, _onMsg, onOpen) => {
      queueMicrotask(() => onOpen && onOpen());
      return { close: jest.fn(), send: jest.fn() };
    });
    gameService.startGame.mockResolvedValue(undefined);
    gameService.leaveGame.mockResolvedValue(undefined);
    gameService.sendGameChat.mockImplementation(() => {});
  });

  test('loads lobby and shows code', async () => {
    renderWithAuth(
      <Routes>
        <Route path="/lobby/:gameId" element={<LobbyPage />} />
      </Routes>,
      { initialEntries: ['/lobby/g1'] },
    );
    await waitFor(() => {
      expect(screen.getByText('ZZZZ')).toBeInTheDocument();
    });
    expect(screen.getByText(/chess lobby/i)).toBeInTheDocument();
  });
});
