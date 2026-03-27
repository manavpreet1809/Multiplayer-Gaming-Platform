import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Profile from './Profile';

describe('Profile component', () => {
    const mockOnBack = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
    });

    function renderProfile(props = {}) {
        return render(
            <Profile
                onBack={mockOnBack}
                username="TestUser"
                email="testuser@example.com"
                {...props}
            />
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

        expect(mockOnBack).toHaveBeenCalled();
    });
});