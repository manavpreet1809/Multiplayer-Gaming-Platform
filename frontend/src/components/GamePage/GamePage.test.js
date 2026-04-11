import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import GamePage from './GamePage';
import { AuthContext } from '../../context/AuthContext';
import {
  getGame,
  createGameWebSocket,
  leaveGame,
} from '../../services/gameService';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
  useParams: () => ({ gameId: '123' }),
}));

jest.mock('../../services/gameService', () => ({
  getGame: jest.fn(),
  createGameWebSocket: jest.fn(),
  leaveGame: jest.fn(),
  sendMove: jest.fn(),
  sendGameChat: jest.fn(),
  sendSelectPiece: jest.fn(),
}));

jest.mock('../ChessBoard/ChessBoard', () => () => <div>ChessBoard</div>);
jest.mock('../TicTacToeBoard/TicTacToeBoard', () => () => <div>TicTacToeBoard</div>);
jest.mock('../GameResults/GameResults', () => () => <div>GameResults</div>);
jest.mock('../Chat/Chat', () => () => <div>Chat Component</div>);

describe('GamePage', () => {
  const renderPage = () =>
    render(
      <AuthContext.Provider value={{ user: { username: 'testuser' } }}>
        <GamePage />
      </AuthContext.Provider>
    );

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('shows loading state initially', () => {
    getGame.mockResolvedValue({});
    createGameWebSocket.mockResolvedValue({ close: jest.fn() });

    renderPage();

    expect(screen.getByText(/Connecting to game/i)).toBeInTheDocument();
  });

  test('renders chess board when game type is chess', async () => {
    getGame.mockResolvedValue({
      game_type: 'chess',
      state: { players: { white: 'testuser' }, activeColor: 'white' },
    });

    createGameWebSocket.mockResolvedValue({ close: jest.fn() });

    renderPage();

    await waitFor(() => {
      expect(screen.getByText('ChessBoard')).toBeInTheDocument();
    });
  });

  test('renders tic tac toe board when game type is tictactoe', async () => {
    getGame.mockResolvedValue({
      game_type: 'tictactoe',
      state: { players: { X: 'testuser' }, currentPlayer: 'X' },
    });

    createGameWebSocket.mockResolvedValue({ close: jest.fn() });

    renderPage();

    await waitFor(() => {
      expect(screen.getByText('TicTacToeBoard')).toBeInTheDocument();
    });
  });

  test('toggles chat panel when chat button is clicked', async () => {
    getGame.mockResolvedValue({
      game_type: 'chess',
      state: { players: { white: 'testuser' }, activeColor: 'white' },
    });

    createGameWebSocket.mockResolvedValue({ close: jest.fn() });

    renderPage();

    await waitFor(() => {
      expect(screen.getByText('ChessBoard')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Chat'));
    expect(screen.getByText('Chat Component')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Close Chat'));
    expect(screen.queryByText('Chat Component')).not.toBeInTheDocument();
  });

  test('calls leaveGame and navigates to dashboard when leaving', async () => {
    getGame.mockResolvedValue({
      game_type: 'chess',
      state: { players: { white: 'testuser' }, activeColor: 'white' },
    });

    createGameWebSocket.mockResolvedValue({ close: jest.fn() });
    leaveGame.mockResolvedValue();

    renderPage();

    await waitFor(() => {
      expect(screen.getByText('ChessBoard')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/Forfeit & Leave/i));

    await waitFor(() => {
      expect(leaveGame).toHaveBeenCalledWith('123');
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});