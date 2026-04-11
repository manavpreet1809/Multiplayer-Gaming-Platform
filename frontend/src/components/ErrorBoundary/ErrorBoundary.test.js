import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary';

// Helper component that throws error
const ProblemChild = ({ shouldThrow }) => {
  if (shouldThrow) {
    throw new Error('Test error');
  }
  return <div>Safe Component</div>;
};

describe('ErrorBoundary', () => {
  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {}); // suppress error logs
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders children when no error occurs', () => {
    render(
      <ErrorBoundary>
        <ProblemChild shouldThrow={false} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Safe Component')).toBeInTheDocument();
  });

  test('displays fallback UI when an error is thrown', () => {
    render(
      <ErrorBoundary>
        <ProblemChild shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  test('shows default error message if no error message is provided', () => {
    const SilentErrorChild = () => {
      throw new Error('');
    };

    render(
      <ErrorBoundary>
        <SilentErrorChild />
      </ErrorBoundary>
    );

    expect(screen.getByText('An unexpected error occurred.')).toBeInTheDocument();
  });

  test('resets error state when "Try Again" is clicked', () => {
    const { rerender } = render(
      <ErrorBoundary>
        <ProblemChild shouldThrow={true} />
      </ErrorBoundary>
    );

    fireEvent.click(screen.getByText('Try Again'));

    rerender(
      <ErrorBoundary>
        <ProblemChild shouldThrow={false} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Safe Component')).toBeInTheDocument();
  });

  test('calls componentDidCatch when error occurs', () => {
    const spy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(
      <ErrorBoundary>
        <ProblemChild shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(spy).toHaveBeenCalled();

    spy.mockRestore();
  });
});