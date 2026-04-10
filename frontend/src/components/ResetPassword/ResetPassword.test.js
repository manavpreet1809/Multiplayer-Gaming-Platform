import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResetPassword from './ResetPassword';
import { resetPassword } from '../../services/authService';

const mockNavigate = jest.fn();

jest.mock('../../services/authService', () => ({
    resetPassword: jest.fn(),
}));

jest.mock('react-router-dom', () => ({
    useNavigate: () => mockNavigate,
}), { virtual: true });

describe('ResetPassword component', () => {
    const mockOnBackToLogin = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        resetPassword.mockResolvedValue(undefined);
    });

    function renderResetPassword(props = {}) {
        return render(
            <ResetPassword
                onBackToLogin={mockOnBackToLogin}
                {...props}
            />
        );
    }

    test('renders initial reset form correctly', () => {
        renderResetPassword();

        expect(screen.getByText(/reset password/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/username or email/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /continue/i })).toBeInTheDocument();
    });

    test('updates identifier input when user types', () => {
        renderResetPassword();

        const input = screen.getByLabelText(/username or email/i);
        fireEvent.change(input, { target: { value: 'user1' } });

        expect(input.value).toBe('user1');
    });

    test('moves to password reset stage after entering identifier and clicking continue', () => {
        renderResetPassword();

        fireEvent.change(screen.getByLabelText(/username or email/i), {
            target: { value: 'user1' },
        });

        fireEvent.click(screen.getByRole('button', { name: /continue/i }));

        expect(screen.getByText(/resetting password for/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/^new password$/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/confirm new password/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /^reset password$/i })).toBeInTheDocument();
    });

    test('calls onResetPassword after valid password submission', async () => {
        renderResetPassword();

        fireEvent.change(screen.getByLabelText(/username or email/i), {
            target: { value: 'user1' },
        });
        fireEvent.click(screen.getByRole('button', { name: /continue/i }));

        fireEvent.change(screen.getByLabelText(/^new password$/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.change(screen.getByLabelText(/confirm new password/i), {
            target: { value: 'ValidPass1!' },
        });

        fireEvent.click(screen.getByRole('button', { name: /^reset password$/i }));

        await waitFor(() => {
            expect(resetPassword).toHaveBeenCalledWith('user1', 'ValidPass1!');
        });
    });

    test('calls onBackToLogin when back button is clicked', () => {
        renderResetPassword();

        fireEvent.change(screen.getByLabelText(/username or email/i), {
            target: { value: 'user1' },
        });
        fireEvent.click(screen.getByRole('button', { name: /continue/i }));
        fireEvent.change(screen.getByLabelText(/^new password$/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.change(screen.getByLabelText(/confirm new password/i), {
            target: { value: 'ValidPass1!' },
        });
        fireEvent.click(screen.getByRole('button', { name: /^reset password$/i }));

        return waitFor(() => {
            fireEvent.click(screen.getAllByRole('button', { name: /back to log in/i })[0]);
            expect(mockOnBackToLogin).toHaveBeenCalled();
        });
    });
});