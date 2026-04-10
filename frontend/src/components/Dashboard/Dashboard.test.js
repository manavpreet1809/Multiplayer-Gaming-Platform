import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from './Dashboard';
import { AuthContext } from '../../context/AuthContext';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    useNavigate: () => mockNavigate,
}), { virtual: true });

describe('Dashboard component', () => {
    const mockLogout = jest.fn();
    const mockOnBrowseGames = jest.fn();
    const mockOnCreateGame = jest.fn();
    const mockOnJoinGame = jest.fn();
    const mockOnEnqueue = jest.fn();
    const mockOnOpenChat = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
    });

    function renderDashboard(props = {}) {
        return render(
            <AuthContext.Provider value={{ user: { username: 'TestUser' }, logout: mockLogout, login: jest.fn() }}>
                <Dashboard
                    onBrowseGames={mockOnBrowseGames}
                    onCreateGame={mockOnCreateGame}
                    onJoinGame={mockOnJoinGame}
                    onEnqueue={mockOnEnqueue}
                    onOpenChat={mockOnOpenChat}
                    {...props}
                />
            </AuthContext.Provider>
        );
    }

    test('renders dashboard with username', () => {
        renderDashboard();

        expect(screen.getByText(/testuser/i)).toBeInTheDocument();
    });

    test('renders navigation options or buttons', () => {
        renderDashboard();

        // Adjust based on your UI if needed
        expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    });

    test('calls onNavigate when a navigation option is clicked', () => {
        renderDashboard();

        fireEvent.click(screen.getByRole('button', { name: /profile/i }));
        expect(mockNavigate).toHaveBeenCalledWith('/profile');
    });

    test('calls onLogout when logout button is clicked', () => {
        renderDashboard();

        const logoutButton = screen.getByRole('button', { name: /logout|log out/i });
        fireEvent.click(logoutButton);

        expect(mockLogout).toHaveBeenCalled();
    });

    test('renders main dashboard container', () => {
        renderDashboard();

        expect(document.body).toBeInTheDocument();
    });
});