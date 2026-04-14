import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import MatchmakePage from './MatchmakePage';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('MatchmakePage', () => {
  beforeEach(() => {
    gameService.matchmake.mockResolvedValue({ game_id: 'mm-1' });
  });

  test('find match navigates to lobby', async () => {
    render(
      <MemoryRouter initialEntries={['/m']}>
        <Routes>
          <Route path="/m" element={<MatchmakePage />} />
          <Route path="/lobby/:gameId" element={<div>Lobby</div>} />
        </Routes>
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole('button', { name: /find match/i }));
    await waitFor(() => expect(gameService.matchmake).toHaveBeenCalledWith('chess'));
    await waitFor(() => expect(screen.getByText('Lobby')).toBeInTheDocument());
  });
});
