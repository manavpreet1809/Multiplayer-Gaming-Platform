import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from './Dashboard';
import { renderWithAuth } from '../../test/testUtils';

describe('Dashboard', () => {
  test('shows username and main actions', () => {
    const onBrowse = jest.fn();
    renderWithAuth(
      <Dashboard
        onBrowseGames={onBrowse}
        onCreateGame={jest.fn()}
        onJoinGame={jest.fn()}
        onEnqueue={jest.fn()}
        onOpenChat={jest.fn()}
        onLeaderboard={jest.fn()}
      />,
    );
    expect(screen.getByText('tester')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /browse games/i }));
    expect(onBrowse).toHaveBeenCalled();
  });
});
