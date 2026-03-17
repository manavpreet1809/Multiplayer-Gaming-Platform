# ChessBoard Component

**Use case**: UC-13 UI — Submit Move (visual only)

8x8 chess board rendered with CSS Grid and Unicode piece symbols. Contains **no game logic** — move validation, turn management, and win detection must be handled externally.

## Board Format

The `board` prop is an 8x8 array where:
- Row 0 = rank 8 (black's back rank)
- Row 7 = rank 1 (white's back rank)
- Uppercase = white pieces: `K` (King), `Q` (Queen), `R` (Rook), `B` (Bishop), `N` (Knight), `P` (Pawn)
- Lowercase = black pieces: `k`, `q`, `r`, `b`, `n`, `p`
- `null` = empty square

If no `board` prop is provided, the component renders the standard starting position.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `board` | `string[][] (8x8)` | No | Piece layout (defaults to starting position) |
| `selectedSquare` | `{ row, col }` | No | Highlighted selected square |
| `highlightedSquares` | `[{ row, col }]` | No | Legal move indicators |
| `lastMove` | `{ from: {row,col}, to: {row,col} }` | No | Last move highlight |
| `currentPlayer` | `"white" \| "black"` | No | Whose turn it is |
| `isMyTurn` | `boolean` | No | Whether local player can interact |
| `onSquareClick(row, col)` | `function` | No | Square click handler |
| `playerColor` | `"white" \| "black"` | No | Local player's color (flips board orientation) |
| `opponentName` | `string` | No | Opponent display name |
| `capturedByWhite` | `string[]` | No | Piece codes captured by white |
| `capturedByBlack` | `string[]` | No | Piece codes captured by black |

## Visual Features

- Classic light/dark square colors (`#f0d9b5` / `#b58863`)
- File (a–h) and rank (1–8) labels
- Board auto-flips when `playerColor="black"`
- Selected square highlight (yellow)
- Legal move dots on empty squares
- Capture rings on occupied squares
- Last-move highlight
- Captured pieces tray above and below the board
- Responsive: shrinks to 44px squares on screens under 600px

## Usage

```jsx
import ChessBoard from './components/ChessBoard';

<ChessBoard
  board={gameState.board}
  selectedSquare={selected}
  highlightedSquares={legalMoves}
  lastMove={gameState.lastMove}
  currentPlayer={gameState.turn}
  isMyTurn={gameState.turn === myColor}
  onSquareClick={(row, col) => handleSquareClick(row, col)}
  playerColor="white"
  opponentName="opponent123"
  capturedByWhite={gameState.capturedWhite}
  capturedByBlack={gameState.capturedBlack}
/>
```
