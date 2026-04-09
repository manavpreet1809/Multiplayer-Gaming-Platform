import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const defaultGameBucket = () => ({
  games_played: 0,
  wins: 0,
  losses: 0,
  ties: 0,
  mmr: 1000,
  rank: 'Bronze',
});

export function renderWithRouter(ui, { initialEntries = ['/'] } = {}) {
  return render(<MemoryRouter initialEntries={initialEntries}>{ui}</MemoryRouter>);
}

export function renderWithAuth(
  ui,
  {
    user = {
      username: 'tester',
      email: 'tester@example.com',
      stats: {
        overall: { ...defaultGameBucket(), games_played: 3, wins: 2, losses: 1, ties: 0 },
        games: {
          chess: { ...defaultGameBucket(), games_played: 2, wins: 1, losses: 1 },
          tictactoe: { ...defaultGameBucket(), games_played: 1, wins: 1, losses: 0 },
        },
      },
    },
    restoring = false,
    login = jest.fn(),
    logout = jest.fn(() => Promise.resolve()),
    initialEntries = ['/'],
  } = {},
) {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      <AuthContext.Provider value={{ user, login, logout, restoring }}>
        {ui}
      </AuthContext.Provider>
    </MemoryRouter>,
  );
}
