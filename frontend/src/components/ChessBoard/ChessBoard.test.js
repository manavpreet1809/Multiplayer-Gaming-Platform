import { render, screen } from '@testing-library/react';
import ChessBoard from './ChessBoard';

describe('ChessBoard component', () => {
    test('renders chess board using role grid', () => {
        render(<ChessBoard />);

        const board = screen.getByRole('grid', { name: /chess board/i });
        expect(board).toBeInTheDocument();
    });

    test('renders multiple squares (buttons)', () => {
        render(<ChessBoard />);

        const squares = screen.getAllByRole('button');
        expect(squares.length).toBeGreaterThan(0);
    });

    test('renders chess pieces on the board', () => {
        render(<ChessBoard />);

        const pieces = document.querySelectorAll('.chess-piece');
        expect(pieces.length).toBeGreaterThan(0);
    });

    test('displays player names correctly', () => {
        render(<ChessBoard />);

        expect(screen.getByText(/You/i)).toBeInTheDocument();
        expect(screen.getByText(/Opponent\s*\(/i)).toBeInTheDocument();
    });

    test('displays current turn information', () => {
        render(<ChessBoard />);

        expect(screen.getByText(/turn/i)).toBeInTheDocument();
    });
});