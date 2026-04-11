import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CreateGamePage from './CreateGamePage';
import { createGame } from '../../services/gameService';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

jest.mock('../../services/gameService', () => ({
  createGame: jest.fn(),
}));

describe('CreateGamePage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders form with default values', () => {
    render(<CreateGamePage />);

    expect(screen.getByText('Create Game')).toBeInTheDocument();
    expect(screen.getByLabelText('Game Type')).toHaveValue('chess');
    expect(screen.getByLabelText('Visibility')).toHaveValue('public');
    expect(screen.getByRole('button', { name: 'Create Lobby' })).toBeInTheDocument();
  });

  test('updates game type and visibility when selections change', () => {
    render(<CreateGamePage />);

    fireEvent.change(screen.getByLabelText('Game Type'), {
      target: { value: 'tictactoe' },
    });
    fireEvent.change(screen.getByLabelText('Visibility'), {
      target: { value: 'private' },
    });

    expect(screen.getByLabelText('Game Type')).toHaveValue('tictactoe');
    expect(screen.getByLabelText('Visibility')).toHaveValue('private');
  });

  test('navigates to dashboard when back button is clicked', () => {
    render(<CreateGamePage />);

    fireEvent.click(screen.getByRole('button', { name: 'Back' }));

    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  test('calls createGame and navigates to lobby on successful submit', async () => {
    createGame.mockResolvedValue({ game_id: 'abc123' });

    render(<CreateGamePage />);

    fireEvent.change(screen.getByLabelText('Game Type'), {
      target: { value: 'tictactoe' },
    });
    fireEvent.change(screen.getByLabelText('Visibility'), {
      target: { value: 'private' },
    });

    fireEvent.click(screen.getByRole('button', { name: 'Create Lobby' }));

    await waitFor(() => {
      expect(createGame).toHaveBeenCalledWith('tictactoe', 'private');
    });

    expect(mockNavigate).toHaveBeenCalledWith('/lobby/abc123');
  });

  test('shows error message when createGame fails', async () => {
    createGame.mockRejectedValue(new Error('Failed to create lobby'));

    render(<CreateGamePage />);

    fireEvent.click(screen.getByRole('button', { name: 'Create Lobby' }));

    await waitFor(() => {
      expect(screen.getByText('Failed to create lobby')).toBeInTheDocument();
    });
  });
});