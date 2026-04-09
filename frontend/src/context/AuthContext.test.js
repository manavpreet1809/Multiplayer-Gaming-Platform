import React, { useContext } from 'react';
import { render, screen, act } from '@testing-library/react';
import { AuthContext, AuthProvider } from './AuthContext';

jest.mock('../services/authService', () => ({
  getMe: jest.fn(() => Promise.resolve({ username: 'boot', stats: {} })),
  getAccessToken: jest.fn(() => null),
  clearTokens: jest.fn(),
}));

function Consumer() {
  const { user, login, restoring } = useContext(AuthContext);
  return (
    <div>
      <span data-testid="restoring">{restoring ? 'yes' : 'no'}</span>
      <span data-testid="user">{user?.username || 'none'}</span>
      <button type="button" onClick={() => login({ username: 'clicked', stats: {} })}>
        set user
      </button>
    </div>
  );
}

describe('AuthProvider', () => {
  test('login updates user', async () => {
    render(
      <AuthProvider>
        <Consumer />
      </AuthProvider>,
    );
    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });
    expect(screen.getByTestId('restoring')).toHaveTextContent('no');
    act(() => {
      screen.getByRole('button', { name: /set user/i }).click();
    });
    expect(screen.getByTestId('user')).toHaveTextContent('clicked');
  });
});
