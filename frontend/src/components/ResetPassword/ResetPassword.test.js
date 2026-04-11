import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ResetPassword from './ResetPassword';

jest.mock('../../services/authService', () => ({
  resetPassword: jest.fn(() => Promise.resolve({})),
}));

const { resetPassword } = require('../../services/authService');

describe('ResetPassword', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('requires identifier on first step', () => {
    render(
      <MemoryRouter>
        <ResetPassword />
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(screen.getByRole('alert')).toHaveTextContent(/enter your username or email/i);
  });

  test('advances to reset step and submits', async () => {
    render(
      <MemoryRouter>
        <ResetPassword />
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText(/username or email/i), { target: { value: 'user1' } });
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(screen.getByText(/resetting password for/i)).toBeInTheDocument();

    const pwd = 'Bb2@bbbb';
    fireEvent.change(screen.getByLabelText(/^new password$/i), { target: { value: pwd } });
    fireEvent.change(screen.getByLabelText(/confirm new password/i), { target: { value: pwd } });
    fireEvent.click(screen.getByRole('button', { name: /reset password/i }));

    await waitFor(() => {
      expect(resetPassword).toHaveBeenCalledWith('user1', pwd);
    });
    expect(await screen.findByText(/password has been reset/i)).toBeInTheDocument();
  });
});
