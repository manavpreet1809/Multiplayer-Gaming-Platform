import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './context/AuthContext';

describe('App', () => {
  test('renders login form at root route', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </MemoryRouter>,
    );
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
  });
});
