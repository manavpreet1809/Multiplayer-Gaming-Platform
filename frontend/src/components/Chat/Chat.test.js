import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Chat from './Chat';

describe('Chat', () => {
  test('shows empty state', () => {
    render(<Chat messages={[]} onSendMessage={jest.fn()} />);
    expect(screen.getByText(/no messages yet/i)).toBeInTheDocument();
  });

  test('sends message', () => {
    const onSend = jest.fn();
    render(
      <Chat
        messages={[{ id: 1, sender: 'a', text: 'hi' }]}
        onSendMessage={onSend}
        context="lobby"
      />,
    );
    expect(screen.getByText('hi')).toBeInTheDocument();
    expect(screen.getByText(/lobby chat/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/chat message/i), { target: { value: 'hello' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));
    expect(onSend).toHaveBeenCalledWith('hello');
  });
});
