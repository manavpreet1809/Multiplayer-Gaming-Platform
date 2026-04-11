import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import BrowseGamesPage from './BrowseGamesPage';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('BrowseGamesPage', () => {
  beforeEach(() => {
    gameService.matchmake.mockResolvedValue({ game_id: 'abc-123' });
  });

  test('matchmake navigates to lobby', async () => {
    render(
      <MemoryRouter initialEntries={['/browse']}>
        <Routes>
          <Route path="/browse" element={<BrowseGamesPage />} />
          <Route path="/lobby/:gameId" element={<div>Lobby page</div>} />
        </Routes>
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole('button', { name: /chess/i }));
    fireEvent.click(screen.getByRole('button', { name: /join lobby/i }));
    await waitFor(() => expect(gameService.matchmake).toHaveBeenCalledWith('chess'));
    await waitFor(() => {
      expect(screen.getByText('Lobby page')).toBeInTheDocument();
    });
  });
});
