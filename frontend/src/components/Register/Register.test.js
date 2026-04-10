import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Register from './Register';
import { AuthContext } from '../../context/AuthContext';
import {
    register as authRegister,
    login as authLogin,
    getMe,
} from '../../services/authService';

const mockNavigate = jest.fn();
const mockLogin = jest.fn();

jest.mock('../../services/authService', () => ({
    register: jest.fn(),
    login: jest.fn(),
    getMe: jest.fn(),
}));

jest.mock('react-router-dom', () => ({
    useNavigate: () => mockNavigate,
}), { virtual: true });

describe('Register component', () => {
    const mockOnLogin = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        authRegister.mockResolvedValue(undefined);
        authLogin.mockResolvedValue({ access_token: 'token' });
        getMe.mockResolvedValue({ username: 'user1', email: 'user1@example.com' });
    });

    function renderRegister(props = {}) {
        return render(
            <AuthContext.Provider value={{ user: null, login: mockLogin, logout: jest.fn() }}>
                <Register
                    onLogin={mockOnLogin}
                    {...props}
                />
            </AuthContext.Provider>
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
        expect(authRegister).not.toHaveBeenCalled();
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
        expect(authRegister).not.toHaveBeenCalled();
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
        expect(authRegister).not.toHaveBeenCalled();
    });

    test('submits valid form and logs user in', async () => {
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
            expect(authRegister).toHaveBeenCalledWith(
                'user1',
                'user1@example.com',
                'ValidPass1!'
            );
        });
        expect(authLogin).toHaveBeenCalledWith('user1', 'ValidPass1!');
        expect(getMe).toHaveBeenCalled();
        expect(mockLogin).toHaveBeenCalledWith({ username: 'user1', email: 'user1@example.com' });
        expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });

    test('shows backend error when registration fails', async () => {
        authRegister.mockRejectedValue(new Error('Email already exists'));
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
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });
});