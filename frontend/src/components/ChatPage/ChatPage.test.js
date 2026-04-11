import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatPage from './ChatPage';
import {
  createGlobalChatWebSocket,
  sendGlobalChat,
} from '../../services/gameService';

const mockNavigate = jest.fn();
const mockClose = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

jest.mock('../../services/gameService', () => ({
  createGlobalChatWebSocket: jest.fn(),
  sendGlobalChat: jest.fn(),
}));

jest.mock('../Chat/Chat', () => (props) => (
  <div data-testid="chat-component">
    <div data-testid="chat-context">{props.context}</div>
    <div data-testid="chat-messages-count">{props.messages.length}</div>
    <button onClick={() => props.onSendMessage('Hello world')}>Mock Send</button>
    {props.messages.map((msg) => (
      <div key={msg.id}>
        {msg.sender}: {msg.text}
      </div>
    ))}
  </div>
));

describe('ChatPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockClose.mockClear();
  });

  test('renders initial connecting state and global chat', async () => {
    createGlobalChatWebSocket.mockResolvedValue({ close: mockClose });

    render(<ChatPage />);

    expect(screen.getByText('Global Chat')).toBeInTheDocument();
    expect(screen.getByText('Connecting…')).toBeInTheDocument();
    expect(screen.getByTestId('chat-context')).toHaveTextContent('global');

    await waitFor(() => {
      expect(createGlobalChatWebSocket).toHaveBeenCalled();
    });
  });

  test('shows connected status when websocket opens', async () => {
    createGlobalChatWebSocket.mockImplementation(async (_onMessage, onOpen) => {
      onOpen();
      return { close: mockClose };
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByText('Connected')).toBeInTheDocument();
    });
  });

  test('loads chat history messages from websocket', async () => {
    createGlobalChatWebSocket.mockImplementation(async (onMessage) => {
      onMessage({
        type: 'history',
        messages: [
          { sender: 'Alice', text: 'Hi' },
          { sender: 'Bob', text: 'Hello' },
        ],
      });
      return { close: mockClose };
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByText('Alice: Hi')).toBeInTheDocument();
      expect(screen.getByText('Bob: Hello')).toBeInTheDocument();
    });

    expect(screen.getByTestId('chat-messages-count')).toHaveTextContent('2');
  });

  test('sends message through sendGlobalChat when Chat triggers onSendMessage', async () => {
    const mockWs = { close: mockClose };

    createGlobalChatWebSocket.mockResolvedValue(mockWs);

    render(<ChatPage />);

    await waitFor(() => {
      expect(createGlobalChatWebSocket).toHaveBeenCalled();
    });

    fireEvent.click(screen.getByText('Mock Send'));

    expect(sendGlobalChat).toHaveBeenCalledWith(mockWs, 'Hello world');
  });

  test('shows error message when websocket connection fails', async () => {
    createGlobalChatWebSocket.mockRejectedValue(new Error('Connection failed'));

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByText('Connection failed')).toBeInTheDocument();
    });

    expect(screen.getByText('Connecting…')).toBeInTheDocument();
  });
});