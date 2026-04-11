import React from 'react';
import { render, screen, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Profile from './Profile';
import { AuthContext } from '../../context/AuthContext';

const userWithStats = {
  username: 'pat',
  email: 'pat@example.com',
  stats: {
    overall: { games_played: 4, wins: 2, losses: 1, ties: 1, mmr: 1015, rank: 'Bronze' },
    games: {
      chess: { games_played: 2, wins: 1, losses: 1, ties: 0, mmr: 1015, rank: 'Bronze' },
      tictactoe: { games_played: 2, wins: 1, losses: 0, ties: 1, mmr: 1015, rank: 'Bronze' },
    },
  },
};

function renderProfile(ctxUser = userWithStats, profileProps = {}) {
  return render(
    <MemoryRouter>
      <AuthContext.Provider
        value={{ user: ctxUser, login: jest.fn(), logout: jest.fn(), restoring: false }}
      >
        <Profile {...profileProps} />
      </AuthContext.Provider>
    </MemoryRouter>,
  );
}

describe('Profile', () => {
  test('shows overall stats from context user', () => {
    renderProfile();
    expect(screen.getByText('pat')).toBeInTheDocument();
    expect(screen.getByText('4')).toBeInTheDocument();
    const winsStat = screen.getByText('Wins').closest('.profile-stat');
    expect(within(winsStat).getByText('2')).toBeInTheDocument();
  });

  test('shows per-game table only for games with plays', () => {
    renderProfile();
    expect(screen.getByText('Chess')).toBeInTheDocument();
    expect(screen.getByText('Tic-Tac-Toe')).toBeInTheDocument();
  });

  test('shows no games message when overall games_played is zero', () => {
    const u = {
      ...userWithStats,
      stats: {
        overall: { games_played: 0, wins: 0, losses: 0, ties: 0, mmr: 1000, rank: 'Bronze' },
        games: { chess: { games_played: 0, wins: 0, losses: 0, ties: 0, mmr: 1000, rank: 'Bronze' }, tictactoe: { games_played: 0, wins: 0, losses: 0, ties: 0, mmr: 1000, rank: 'Bronze' } },
      },
    };
    renderProfile(u);
    expect(screen.getByText(/no games played yet/i)).toBeInTheDocument();
  });
});
