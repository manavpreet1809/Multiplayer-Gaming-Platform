import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary';

function Boom() {
  throw new Error('Test explosion');
}

describe('ErrorBoundary', () => {
  const err = console.error;
  beforeAll(() => {
    console.error = jest.fn();
  });
  afterAll(() => {
    console.error = err;
  });

  test('renders children when no error', () => {
    render(
      <ErrorBoundary>
        <div>OK</div>
      </ErrorBoundary>,
    );
    expect(screen.getByText('OK')).toBeInTheDocument();
  });

  test('shows fallback on child error', () => {
    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>,
    );
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    expect(screen.getByText(/test explosion/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
  });

  test('Try Again re-renders children after error', () => {
    let shouldThrow = true;
    function MaybeBoom() {
      if (shouldThrow) throw new Error('boom');
      return <div>Recovered</div>;
    }

    render(
      <ErrorBoundary>
        <MaybeBoom />
      </ErrorBoundary>,
    );
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    shouldThrow = false;
    fireEvent.click(screen.getByRole('button', { name: /try again/i }));
    expect(screen.getByText('Recovered')).toBeInTheDocument();
  });
});
