import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from './Login';

describe('Login component', () => {
  const mockOnLogin = jest.fn();
  const mockOnForgotPassword = jest.fn();
  const mockOnRegister = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    mockOnLogin.mockResolvedValue(undefined);
  });

  function renderLogin(props = {}) {
    return render(
      <Login
        onLogin={mockOnLogin}
        onForgotPassword={mockOnForgotPassword}
        onRegister={mockOnRegister}
        {...props}
      />
    );
  }

  test('renders the login form with all fields', () => {
    renderLogin();
    expect(screen.getByLabelText(/username or email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
  });

  test('renders forgot password and register links', () => {
    renderLogin();
    expect(screen.getByText(/forgot password/i)).toBeInTheDocument();
    expect(screen.getByText(/create an account/i)).toBeInTheDocument();
  });

  test('shows validation error when fields are empty', () => {
    renderLogin();
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));
    expect(screen.getByRole('alert')).toHaveTextContent(
      /please enter your username\/email and password/i
    );
    expect(mockOnLogin).not.toHaveBeenCalled();
  });

  test('calls onLogin with identifier and password on submit', async () => {
    renderLogin();
    fireEvent.change(screen.getByLabelText(/username or email/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(mockOnLogin).toHaveBeenCalledWith('testuser', 'password123');
    });
  });

  test('displays error message when onLogin rejects', async () => {
    mockOnLogin.mockRejectedValue(new Error('Invalid credentials'));
    renderLogin();

    fireEvent.change(screen.getByLabelText(/username or email/i), {
      target: { value: 'bad' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrong' },
    });
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/invalid credentials/i);
    });
  });

  test('calls onForgotPassword when link is clicked', () => {
    renderLogin();
    fireEvent.click(screen.getByText(/forgot password/i));
    expect(mockOnForgotPassword).toHaveBeenCalled();
  });

  test('calls onRegister when link is clicked', () => {
    renderLogin();
    fireEvent.click(screen.getByText(/create an account/i));
    expect(mockOnRegister).toHaveBeenCalled();
  });

  test('hides forgot password link when callback not provided', () => {
    renderLogin({ onForgotPassword: undefined });
    expect(screen.queryByText(/forgot password/i)).not.toBeInTheDocument();
  });

  test('hides register link when callback not provided', () => {
    renderLogin({ onRegister: undefined });
    expect(screen.queryByText(/create an account/i)).not.toBeInTheDocument();
  });
});
