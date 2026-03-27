import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Register from './Register';

describe('Register component', () => {
    const mockOnRegister = jest.fn();
    const mockOnLogin = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        mockOnRegister.mockResolvedValue(undefined);
    });

    function renderRegister(props = {}) {
        return render(
            <Register
                onRegister={mockOnRegister}
                onLogin={mockOnLogin}
                {...props}
            />
        );
    }

    test('renders the registration form with all fields', () => {
        renderRegister();

        expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/^email$/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
    });

    test('shows validation error when required fields are empty', () => {
        renderRegister();

        fireEvent.click(screen.getByRole('button', { name: /create account/i }));

        expect(screen.getByRole('alert')).toHaveTextContent(/all fields are required/i);
        expect(mockOnRegister).not.toHaveBeenCalled();
    });

    test('shows validation error when passwords do not match', () => {
        renderRegister();

        fireEvent.change(screen.getByLabelText(/username/i), {
            target: { value: 'user1' },
        });
        fireEvent.change(screen.getByLabelText(/^email$/i), {
            target: { value: 'user1@example.com' },
        });
        fireEvent.change(screen.getByLabelText(/^password$/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: 'DifferentPass1!' },
        });

        fireEvent.click(screen.getByRole('button', { name: /create account/i }));

        expect(screen.getByRole('alert')).toHaveTextContent(/passwords do not match/i);
        expect(mockOnRegister).not.toHaveBeenCalled();
    });

    test('shows password rule validation error for weak password', () => {
        renderRegister();

        fireEvent.change(screen.getByLabelText(/username/i), {
            target: { value: 'user1' },
        });
        fireEvent.change(screen.getByLabelText(/^email$/i), {
            target: { value: 'user1@example.com' },
        });
        fireEvent.change(screen.getByLabelText(/^password$/i), {
            target: { value: 'weak' },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: 'weak' },
        });

        fireEvent.click(screen.getByRole('button', { name: /create account/i }));

        expect(screen.getByRole('alert')).toHaveTextContent(/password must contain/i);
        expect(mockOnRegister).not.toHaveBeenCalled();
    });

    test('calls onRegister with trimmed username and email when form is valid', async () => {
        renderRegister();

        fireEvent.change(screen.getByLabelText(/username/i), {
            target: { value: '  user1  ' },
        });
        fireEvent.change(screen.getByLabelText(/^email$/i), {
            target: { value: '  user1@example.com  ' },
        });
        fireEvent.change(screen.getByLabelText(/^password$/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: 'ValidPass1!' },
        });

        fireEvent.click(screen.getByRole('button', { name: /create account/i }));

        await waitFor(() => {
            expect(mockOnRegister).toHaveBeenCalledWith(
                'user1',
                'user1@example.com',
                'ValidPass1!'
            );
        });
    });

    test('shows backend error when registration fails', async () => {
        mockOnRegister.mockRejectedValue(new Error('Email already exists'));
        renderRegister();

        fireEvent.change(screen.getByLabelText(/username/i), {
            target: { value: 'user1' },
        });
        fireEvent.change(screen.getByLabelText(/^email$/i), {
            target: { value: 'user1@example.com' },
        });
        fireEvent.change(screen.getByLabelText(/^password$/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: 'ValidPass1!' },
        });

        fireEvent.click(screen.getByRole('button', { name: /create account/i }));

        await waitFor(() => {
            expect(screen.getByRole('alert')).toHaveTextContent(/email already exists/i);
        });
    });

    test('calls onLogin when login link is clicked', () => {
        renderRegister();

        fireEvent.click(screen.getByRole('button', { name: /already have an account\? log in/i }));
        expect(mockOnLogin).toHaveBeenCalled();
    });
});