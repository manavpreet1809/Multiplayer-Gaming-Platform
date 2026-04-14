import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import { AuthContext } from '../../context/AuthContext';

function renderProtected({ user = null, restoring = false } = {}) {
  return render(
    <MemoryRouter initialEntries={['/secret']}>
      <AuthContext.Provider value={{ user, login: jest.fn(), logout: jest.fn(), restoring }}>
        <Routes>
          <Route
            path="/secret"
            element={
              <ProtectedRoute>
                <div>Secret content</div>
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<div>Login page</div>} />
        </Routes>
      </AuthContext.Provider>
    </MemoryRouter>,
  );
}

describe('ProtectedRoute', () => {
  test('redirects to home when no user and not restoring', () => {
    renderProtected({ user: null, restoring: false });
    expect(screen.getByText('Login page')).toBeInTheDocument();
    expect(screen.queryByText('Secret content')).not.toBeInTheDocument();
  });

  test('renders children when user present', () => {
    renderProtected({ user: { username: 'u' }, restoring: false });
    expect(screen.getByText('Secret content')).toBeInTheDocument();
  });

  test('renders nothing while restoring', () => {
    const { container } = renderProtected({ user: null, restoring: true });
    expect(container.firstChild).toBeNull();
  });
});
