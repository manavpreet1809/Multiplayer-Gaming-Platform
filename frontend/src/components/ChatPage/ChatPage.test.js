import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ChatPage from './ChatPage';

jest.mock('../../services/gameService');

const gameService = require('../../services/gameService');

describe('ChatPage', () => {
  beforeEach(() => {
    gameService.createGlobalChatWebSocket.mockImplementation(async (_onMsg, onOpen) => {
      queueMicrotask(() => onOpen && onOpen());
      return { close: jest.fn(), send: jest.fn() };
    });
    gameService.sendGlobalChat.mockImplementation(() => {});
  });

  test('renders global chat header', async () => {
    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>,
    );
    expect(screen.getByRole('heading', { level: 2, name: /global chat/i })).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/connected/i)).toBeInTheDocument();
    });
  });
});
