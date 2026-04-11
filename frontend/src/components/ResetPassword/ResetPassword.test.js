import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResetPassword from './ResetPassword';

describe('ResetPassword component', () => {
    const mockOnResetPassword = jest.fn();
    const mockOnBackToLogin = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        mockOnResetPassword.mockResolvedValue(undefined);
    });

    function renderResetPassword(props = {}) {
        return render(
            <ResetPassword
                onResetPassword={mockOnResetPassword}
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
            expect(mockOnResetPassword).toHaveBeenCalled();
        });
    });

    test('calls onBackToLogin when back button is clicked', () => {
        renderResetPassword();

        fireEvent.click(screen.getByRole('button', { name: /back to log in/i }));

        expect(mockOnBackToLogin).toHaveBeenCalled();
    });
});