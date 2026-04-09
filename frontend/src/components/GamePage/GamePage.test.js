import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import { Routes, Route } from 'react-router-dom';
import GamePage from './GamePage';
import { renderWithAuth } from '../../test/testUtils';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('GamePage', () => {
  beforeEach(() => {
    gameService.getGame.mockRejectedValue(new Error('Game not found'));
    gameService.createGameWebSocket.mockResolvedValue({ close: jest.fn(), send: jest.fn() });
    gameService.leaveGame.mockResolvedValue(undefined);
    gameService.sendMove.mockImplementation(() => {});
    gameService.sendGameChat.mockImplementation(() => {});
    gameService.sendSelectPiece.mockImplementation(() => {});
  });

  test('shows error when getGame fails', async () => {
    renderWithAuth(
      <Routes>
        <Route path="/game/:gameId" element={<GamePage />} />
      </Routes>,
      { initialEntries: ['/game/missing'] },
    );
    await waitFor(() => {
      expect(screen.getByText(/game not found/i)).toBeInTheDocument();
    });
  });
});
