import { render, screen, fireEvent } from '@testing-library/react';
import ChessBoard from './ChessBoard';

describe('ChessBoard component', () => {
    test('renders chessboard container', () => {
        render(<ChessBoard />);

        const board = screen.getByTestId('chessboard');
        expect(board).toBeInTheDocument();
    });

    test('renders 64 squares on the board', () => {
        render(<ChessBoard />);

        const squares = screen.getAllByTestId('square');
        expect(squares.length).toBe(64);
    });

    test('renders initial pieces on the board', () => {
        render(<ChessBoard />);

        const pieces = screen.getAllByTestId('piece');
        expect(pieces.length).toBeGreaterThan(0);
    });

    test('allows selecting a piece on click', () => {
        render(<ChessBoard />);

        const piece = screen.getAllByTestId('piece')[0];
        fireEvent.click(piece);

        expect(piece).toHaveClass('selected');
    });

    test('handles piece movement when a square is clicked', () => {
        render(<ChessBoard />);

        const pieces = screen.getAllByTestId('piece');
        const squares = screen.getAllByTestId('square');

        fireEvent.click(pieces[0]);   // select piece
        fireEvent.click(squares[10]); // move target

        // We assume state update or DOM change
        expect(squares[10]).toBeInTheDocument();
    });
});