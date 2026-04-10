import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Profile from './Profile';
import { AuthContext } from '../../context/AuthContext';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    useNavigate: () => mockNavigate,
}), { virtual: true });

describe('Profile component', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    function renderProfile(props = {}) {
        return render(
            <AuthContext.Provider
                value={{ user: { username: 'TestUser', email: 'testuser@example.com' }, login: jest.fn(), logout: jest.fn() }}
            >
                <Profile {...props} />
            </AuthContext.Provider>
        );
    }

    test('renders profile heading and user information', () => {
        renderProfile();

        expect(screen.getByText(/player profile/i)).toBeInTheDocument();
        expect(screen.getByText(/^TestUser$/i)).toBeInTheDocument(); // FIXED
        expect(screen.getByText(/testuser@example.com/i)).toBeInTheDocument();
    });

    test('renders profile labels correctly', () => {
        renderProfile();

        expect(screen.getByText(/username/i)).toBeInTheDocument();
        expect(screen.getByText(/email/i)).toBeInTheDocument();
    });

    test('displays stats section', () => {
        renderProfile();

        expect(screen.getByText(/overall stats/i)).toBeInTheDocument();
    });

    test('shows empty stats message when no data', () => {
        renderProfile();

        expect(screen.getByText(/no games played yet/i)).toBeInTheDocument();
    });

    test('calls onBack when back button is clicked', () => {
        renderProfile();

        fireEvent.click(screen.getByRole('button', { name: /back to dashboard/i }));

        expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
});