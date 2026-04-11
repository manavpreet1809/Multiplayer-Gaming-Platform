import React from 'react';
import { render, screen } from '@testing-library/react';
import { Routes, Route } from 'react-router-dom';
import DashboardPage from './DashboardPage';
import { renderWithAuth } from '../../test/testUtils';

describe('DashboardPage', () => {
  test('renders dashboard with navigation wiring', () => {
    renderWithAuth(
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>,
      { initialEntries: ['/dashboard'] },
    );
    expect(screen.getByRole('heading', { name: /dashboard/i })).toBeInTheDocument();
  });
});
