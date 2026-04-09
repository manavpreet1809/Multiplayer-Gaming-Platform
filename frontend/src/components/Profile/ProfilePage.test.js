import React, { useState, useCallback } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ProfilePage from './ProfilePage';
import { AuthContext } from '../../context/AuthContext';

jest.mock('../../services/authService', () => ({
  ...jest.requireActual('../../services/authService'),
  getMe: jest.fn(),
}));

const authService = require('../../services/authService');

const refreshedUser = {
  username: 'refreshed',
  email: 'r@example.com',
  stats: {
    overall: { games_played: 1, wins: 1, losses: 0, ties: 0, mmr: 1025, rank: 'Bronze' },
    games: {
      chess: { games_played: 1, wins: 1, losses: 0, ties: 0, mmr: 1025, rank: 'Bronze' },
      tictactoe: { games_played: 0, wins: 0, losses: 0, ties: 0, mmr: 1000, rank: 'Bronze' },
    },
  },
};

function ProfileHarness() {
  const [user, setUser] = useState(null);
  const login = useCallback((u) => setUser(u), []);
  return (
    <AuthContext.Provider
      value={{ user, login, logout: jest.fn(() => Promise.resolve()), restoring: false }}
    >
      <ProfilePage />
    </AuthContext.Provider>
  );
}

describe('ProfilePage', () => {
  beforeEach(() => {
    authService.getMe.mockResolvedValue(refreshedUser);
  });

  test('refreshes user via getMe and updates profile display', async () => {
    render(
      <MemoryRouter>
        <ProfileHarness />
      </MemoryRouter>,
    );

    expect(screen.getByText(/loading profile/i)).toBeInTheDocument();
    await waitFor(() => expect(authService.getMe).toHaveBeenCalled());
    await waitFor(() => {
      expect(screen.getByText('refreshed')).toBeInTheDocument();
    });
  });
});
