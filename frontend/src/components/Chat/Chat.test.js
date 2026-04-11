import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Chat from './Chat';

describe('Chat Component', () => {
  const mockSend = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders Global Chat title by default', () => {
    render(<Chat onSendMessage={mockSend} />);
    expect(screen.getByText('Global Chat')).toBeInTheDocument();
  });

  test('renders Lobby Chat title when context is lobby', () => {
    render(<Chat context="lobby" onSendMessage={mockSend} />);
    expect(screen.getByText('Lobby Chat')).toBeInTheDocument();
  });

  test('shows empty message when no messages are provided', () => {
    render(<Chat messages={[]} onSendMessage={mockSend} />);
    expect(screen.getByText('No messages yet.')).toBeInTheDocument();
  });

  test('renders messages correctly', () => {
    const messages = [
      { id: 1, sender: 'Alice', text: 'Hello', timestamp: '10:00' },
    ];

    render(<Chat messages={messages} onSendMessage={mockSend} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('10:00')).toBeInTheDocument();
  });

  test('sends message and clears input on submit', () => {
    render(<Chat onSendMessage={mockSend} />);

    const input = screen.getByLabelText('Chat message');
    const button = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hi there' } });
    fireEvent.click(button);

    expect(mockSend).toHaveBeenCalledWith('Hi there');
    expect(input.value).toBe('');
  });
});