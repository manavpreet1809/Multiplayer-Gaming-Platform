import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Leaderboard from './Leaderboard';

function renderLeaderboard(props = {}) {
  return render(
    <MemoryRouter>
      <Leaderboard
        gameTypes={['Overall', 'Chess']}
        selectedGameType="Overall"
        onSelectGameType={jest.fn()}
        rankings={[
          { place: 1, username: 'alice', tier: 'Gold', mmr: 1500, wins: 10, losses: 2, ties: 1 },
          { place: 2, username: 'bob', tier: 'Silver', mmr: 1300, wins: 5, losses: 5, ties: 0 },
        ]}
        currentUsername="alice"
        {...props}
      />
    </MemoryRouter>,
  );
}

describe('Leaderboard', () => {
  test('renders ordinal place and tier columns', () => {
    renderLeaderboard();
    expect(screen.getByRole('columnheader', { name: '#' })).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('alice')).toBeInTheDocument();
    expect(screen.getByText('Gold')).toBeInTheDocument();
    expect(screen.getByText('10/2/1')).toBeInTheDocument();
  });

  test('highlights current user row', () => {
    const { container } = renderLeaderboard();
    const row = container.querySelector('.leaderboard-row--current');
    expect(row).toBeTruthy();
    expect(row).toHaveTextContent('alice');
  });

  test('calls onSelectGameType when tab clicked', () => {
    const onSelect = jest.fn();
    renderLeaderboard({ onSelectGameType: onSelect });
    fireEvent.click(screen.getByRole('button', { name: 'Chess' }));
    expect(onSelect).toHaveBeenCalledWith('Chess');
  });

  test('shows empty message when no rankings', () => {
    render(
      <MemoryRouter>
        <Leaderboard rankings={[]} gameTypes={[]} />
      </MemoryRouter>,
    );
    expect(screen.getByText(/no rankings available/i)).toBeInTheDocument();
  });

  test('falls back to index+1 when place omitted', () => {
    render(
      <MemoryRouter>
        <Leaderboard
          rankings={[{ username: 'solo', tier: 'Bronze', mmr: 1000, wins: 0, losses: 0, ties: 0 }]}
          gameTypes={[]}
        />
      </MemoryRouter>,
    );
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
