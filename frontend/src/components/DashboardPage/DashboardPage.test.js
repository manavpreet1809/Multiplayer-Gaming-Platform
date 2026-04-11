import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DashboardPage from './DashboardPage';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

jest.mock('../Dashboard/Dashboard', () => (props) => (
  <div>
    <button onClick={props.onBrowseGames}>Browse</button>
    <button onClick={props.onCreateGame}>Create</button>
    <button onClick={props.onJoinGame}>Join</button>
    <button onClick={props.onEnqueue}>Matchmake</button>
    <button onClick={props.onOpenChat}>Chat</button>
    <button onClick={props.onLeaderboard}>Leaderboard</button>
  </div>
));

describe('DashboardPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('navigates to browse page', () => {
    render(<DashboardPage />);
    fireEvent.click(screen.getByText('Browse'));
    expect(mockNavigate).toHaveBeenCalledWith('/browse');
  });

  test('navigates to create game page', () => {
    render(<DashboardPage />);
    fireEvent.click(screen.getByText('Create'));
    expect(mockNavigate).toHaveBeenCalledWith('/create-game');
  });

  test('navigates to join game page', () => {
    render(<DashboardPage />);
    fireEvent.click(screen.getByText('Join'));
    expect(mockNavigate).toHaveBeenCalledWith('/join-game');
  });

  test('navigates to matchmaking page', () => {
    render(<DashboardPage />);
    fireEvent.click(screen.getByText('Matchmake'));
    expect(mockNavigate).toHaveBeenCalledWith('/matchmake');
  });

  test('navigates to chat and leaderboard pages', () => {
    render(<DashboardPage />);

    fireEvent.click(screen.getByText('Chat'));
    expect(mockNavigate).toHaveBeenCalledWith('/chat');

    fireEvent.click(screen.getByText('Leaderboard'));
    expect(mockNavigate).toHaveBeenCalledWith('/leaderboard');
  });
});