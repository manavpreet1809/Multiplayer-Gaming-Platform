import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ScreenshotPage from './ScreenshotPage';
import { AuthContext } from './context/AuthContext';

const noop = () => {};

describe('ScreenshotPage', () => {
  test('renders known screenshot anchor ids', () => {
    const { container } = render(
      <MemoryRouter>
        <AuthContext.Provider
          value={{ user: null, login: noop, logout: noop, restoring: false }}
        >
          <ScreenshotPage />
        </AuthContext.Provider>
      </MemoryRouter>,
    );
    expect(container.querySelector('#ss-login')).toBeInTheDocument();
    expect(container.querySelector('#ss-dashboard')).toBeInTheDocument();
    expect(container.querySelector('#ss-register')).toBeInTheDocument();
  });
});
