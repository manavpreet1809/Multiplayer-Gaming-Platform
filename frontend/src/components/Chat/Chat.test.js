import { render, screen, fireEvent } from '@testing-library/react';
import Chat from './Chat';

describe('Chat component', () => {
    test('renders Global Chat title by default', () => {
        render(<Chat />);

        expect(screen.getByText('Global Chat')).toBeInTheDocument();
    });

    test('renders Lobby Chat title when context is lobby', () => {
        render(<Chat context="lobby" />);

        expect(screen.getByText('Lobby Chat')).toBeInTheDocument();
    });

    test('shows empty state message when there are no messages', () => {
        render(<Chat messages={[]} />);

        expect(screen.getByText('No messages yet.')).toBeInTheDocument();
    });

    test('renders provided messages with sender, text, and timestamp', () => {
        const messages = [
            { id: '1', sender: 'User1', text: 'Hello there', timestamp: '10:30 AM' },
            { id: '2', sender: 'User2', text: 'Welcome!', timestamp: '10:31 AM' },
        ];

        render(<Chat messages={messages} />);

        expect(screen.getByText('User1')).toBeInTheDocument();
        expect(screen.getByText('Hello there')).toBeInTheDocument();
        expect(screen.getByText('10:30 AM')).toBeInTheDocument();

        expect(screen.getByText('User2')).toBeInTheDocument();
        expect(screen.getByText('Welcome!')).toBeInTheDocument();
        expect(screen.getByText('10:31 AM')).toBeInTheDocument();
    });

    test('calls onSendMessage with trimmed input and clears the input field', () => {
        const mockSendMessage = jest.fn();

        render(<Chat onSendMessage={mockSendMessage} />);

        const input = screen.getByLabelText('Chat message');
        const sendButton = screen.getByRole('button', { name: 'Send' });

        fireEvent.change(input, { target: { value: '   Hello everyone   ' } });
        fireEvent.click(sendButton);

        expect(mockSendMessage).toHaveBeenCalledTimes(1);
        expect(mockSendMessage).toHaveBeenCalledWith('Hello everyone');
        expect(input.value).toBe('');
    });
});