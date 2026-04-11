import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Register from './Register';
import { AuthContext } from '../../context/AuthContext';

const mockRegister = jest.fn();
const mockLogin = jest.fn();
const mockGetMe = jest.fn();

jest.mock('../../services/authService', () => ({
  register: (...a) => mockRegister(...a),
  login: (...a) => mockLogin(...a),
  getMe: (...a) => mockGetMe(...a),
}));

describe('Register', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockRegister.mockResolvedValue({});
    mockLogin.mockResolvedValue({});
    mockGetMe.mockResolvedValue({ username: 'newu', email: 'e@e.com', stats: {} });
  });

  function renderRegister() {
    return render(
      <MemoryRouter>
        <AuthContext.Provider
          value={{ user: null, login: jest.fn(), logout: jest.fn(), restoring: false }}
        >
          <Register />
        </AuthContext.Provider>
      </MemoryRouter>,
    );
  }

  test('shows error when fields empty', async () => {
    renderRegister();
    fireEvent.click(screen.getByRole('button', { name: /create account/i }));
    expect(await screen.findByRole('alert')).toHaveTextContent(/all fields are required/i);
    expect(mockRegister).not.toHaveBeenCalled();
  });

  test('shows error when passwords do not match', async () => {
    renderRegister();
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'u1' } });
    fireEvent.change(screen.getByLabelText(/^email$/i), { target: { value: 'u1@e.com' } });
    fireEvent.change(screen.getByLabelText(/^password$/i), { target: { value: 'Aa1!aaaa' } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: 'Bb1!bbbb' } });
    fireEvent.click(screen.getByRole('button', { name: /create account/i }));
    expect(await screen.findByRole('alert')).toHaveTextContent(/passwords do not match/i);
  });

  test('submits valid registration', async () => {
    const ctxLogin = jest.fn();
    render(
      <MemoryRouter>
        <AuthContext.Provider
          value={{ user: null, login: ctxLogin, logout: jest.fn(), restoring: false }}
        >
          <Register />
        </AuthContext.Provider>
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'u1' } });
    fireEvent.change(screen.getByLabelText(/^email$/i), { target: { value: 'u1@e.com' } });
    const pwd = 'Aa1!aaaa';
    fireEvent.change(screen.getByLabelText(/^password$/i), { target: { value: pwd } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: pwd } });
    fireEvent.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith('u1', 'u1@e.com', pwd);
    });
    await waitFor(() => expect(ctxLogin).toHaveBeenCalled());
  });
});
