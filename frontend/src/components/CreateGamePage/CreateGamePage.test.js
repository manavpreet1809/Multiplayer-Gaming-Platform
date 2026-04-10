import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import CreateGamePage from './CreateGamePage';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('CreateGamePage', () => {
  beforeEach(() => {
    gameService.createGame.mockResolvedValue({ game_id: 'new-game' });
  });

  test('submits and navigates to lobby', async () => {
    render(
      <MemoryRouter initialEntries={['/create']}>
        <Routes>
          <Route path="/create" element={<CreateGamePage />} />
          <Route path="/lobby/:gameId" element={<div>Lobby</div>} />
        </Routes>
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole('button', { name: /create lobby/i }));
    await waitFor(() => expect(gameService.createGame).toHaveBeenCalled());
    await waitFor(() => expect(screen.getByText('Lobby')).toBeInTheDocument());
  });
});
