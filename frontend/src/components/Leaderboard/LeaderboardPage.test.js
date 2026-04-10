import React from 'react';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import LeaderboardPage from './LeaderboardPage';
import { renderWithAuth } from '../../test/testUtils';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('LeaderboardPage', () => {
  beforeEach(() => {
    gameService.getLeaderboard.mockResolvedValue([
      { place: 1, username: 'x', tier: 'Bronze', mmr: 1000, wins: 0, losses: 0, ties: 0 },
    ]);
  });

  test('loads leaderboard for selected game type', async () => {
    renderWithAuth(<LeaderboardPage />);
    await waitFor(() => {
      expect(gameService.getLeaderboard).toHaveBeenCalledWith('overall');
    });
    await waitFor(() => {
      expect(screen.getByText('x')).toBeInTheDocument();
    });
  });

  test('refetches when game type tab changes', async () => {
    renderWithAuth(<LeaderboardPage />);
    await waitFor(() => expect(gameService.getLeaderboard).toHaveBeenCalledWith('overall'));
    gameService.getLeaderboard.mockResolvedValueOnce([
      { place: 1, username: 'y', tier: 'Gold', mmr: 1600, wins: 3, losses: 0, ties: 0 },
    ]);
    const chessTab = await screen.findByRole('button', { name: 'Chess' });
    fireEvent.click(chessTab);
    await waitFor(() => {
      expect(gameService.getLeaderboard).toHaveBeenCalledWith('chess');
    });
  });
});
