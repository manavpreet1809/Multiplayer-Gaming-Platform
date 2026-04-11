import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Dashboard from './Dashboard';
import { AuthContext } from '../../context/AuthContext';

const mockNavigate = jest.fn();
const mockLogout = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('Dashboard', () => {
  const defaultProps = {
    status: 'idle',
    notifications: [],
    onBrowseGames: jest.fn(),
    onCreateGame: jest.fn(),
    onJoinGame: jest.fn(),
    onEnqueue: jest.fn(),
    onOpenChat: jest.fn(),
    onJoinActiveGame: jest.fn(),
    onLeaderboard: jest.fn(),
  };

  const renderWithAuth = (props = {}) =>
    render(
      <AuthContext.Provider value={{ user: { username: 'testuser' }, logout: mockLogout }}>
        <Dashboard {...defaultProps} {...props} />
      </AuthContext.Provider>
    );

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders dashboard title, username, and idle status', () => {
    renderWithAuth();

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('testuser')).toBeInTheDocument();
    expect(screen.getByText('idle')).toBeInTheDocument();
  });

  test('renders notifications when provided', () => {
    renderWithAuth({
      notifications: [
        { id: 1, message: 'Game invite received' },
        { id: 2, message: 'Leaderboard updated' },
      ],
    });

    expect(screen.getByText('Notifications')).toBeInTheDocument();
    expect(screen.getByText('Game invite received')).toBeInTheDocument();
    expect(screen.getByText('Leaderboard updated')).toBeInTheDocument();
  });

  test('calls action handlers when action buttons are clicked', () => {
    renderWithAuth();

    fireEvent.click(screen.getByText('Browse Games'));
    fireEvent.click(screen.getByText('Create Game'));
    fireEvent.click(screen.getByText('Join Game'));
    fireEvent.click(screen.getByText('Find Match'));
    fireEvent.click(screen.getByText('Open Chat'));

    expect(defaultProps.onBrowseGames).toHaveBeenCalled();
    expect(defaultProps.onCreateGame).toHaveBeenCalled();
    expect(defaultProps.onJoinGame).toHaveBeenCalled();
    expect(defaultProps.onEnqueue).toHaveBeenCalled();
    expect(defaultProps.onOpenChat).toHaveBeenCalled();
  });

  test('renders game-ready banner and calls onJoinActiveGame', () => {
    renderWithAuth({ status: 'game-ready' });

    expect(screen.getByText('A game is ready for you!')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Join Game'));
    expect(defaultProps.onJoinActiveGame).toHaveBeenCalled();
  });

  test('logs out and navigates to home when logout is clicked', async () => {
    mockLogout.mockResolvedValue();

    renderWithAuth();

    fireEvent.click(screen.getByText('Log Out'));

    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });
});