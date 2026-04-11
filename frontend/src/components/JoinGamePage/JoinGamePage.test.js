import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import JoinGamePage from './JoinGamePage';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('JoinGamePage', () => {
  beforeEach(() => {
    gameService.joinGameByCode.mockResolvedValue({ game_id: 'joined-1' });
  });

  test('joins with code and navigates', async () => {
    render(
      <MemoryRouter initialEntries={['/join']}>
        <Routes>
          <Route path="/join" element={<JoinGamePage />} />
          <Route path="/lobby/:gameId" element={<div>Lobby here</div>} />
        </Routes>
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText(/lobby code/i), { target: { value: 'ABCD' } });
    fireEvent.click(screen.getByRole('button', { name: /join lobby/i }));
    await waitFor(() => expect(gameService.joinGameByCode).toHaveBeenCalledWith('ABCD'));
    await waitFor(() => expect(screen.getByText('Lobby here')).toBeInTheDocument());
  });
});
