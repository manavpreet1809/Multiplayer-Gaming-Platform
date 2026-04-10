import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { AuthContext } from './context/AuthContext';

jest.mock('react-router-dom', () => ({
  useNavigate: () => jest.fn(),
  Routes: ({ children }) => {
    const firstRoute = Array.isArray(children) ? children[0] : children;
    return firstRoute?.props?.element ?? null;
  },
  Route: () => null,
}), { virtual: true });

test('renders login form by default', () => {
  render(
    <AuthContext.Provider value={{ user: null, login: jest.fn(), logout: jest.fn() }}>
      <App />
    </AuthContext.Provider>
  );
  expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
});
