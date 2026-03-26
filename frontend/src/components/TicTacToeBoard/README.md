# TicTacToeBoard Component

**Use case**: UC-13 UI — Submit Move (visual only)

3x3 Tic-Tac-Toe board rendered with CSS Grid. Contains **no game logic** — move validation, turn management, and win detection must be handled externally.

## Board Format

The `board` prop is a flat array of 9 values:

```
Index layout:
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
```

Each cell is `"X"`, `"O"`, or `null` (empty).

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `board` | `("X" \| "O" \| null)[]` | No | 9-cell array (defaults to all `null`) |
| `winningCells` | `number[]` | No | Indices forming the winning line (e.g. `[0, 1, 2]`) |
| `currentPlayer` | `"X" \| "O"` | No | Whose turn it is |
| `isMyTurn` | `boolean` | No | Whether local player can interact |
| `onCellClick(index)` | `function` | No | Cell click handler |
| `playerSymbol` | `"X" \| "O"` | No | Local player's mark |
| `opponentName` | `string` | No | Opponent display name |

## Visual Features

- X marks in blue (`#1976d2`), O marks in red (`#d32f2f`)
- Winning cells highlighted in green
- Turn indicator with active-player highlight
- Cells disabled when: not your turn, cell occupied, or game over
- Accessible `aria-label` on each cell

## Usage

```jsx
import TicTacToeBoard from './components/TicTacToeBoard';

<TicTacToeBoard
  board={['X', null, 'O', null, 'X', null, null, null, 'O']}
  currentPlayer="X"
  isMyTurn={true}
  onCellClick={(index) => makeMove(index)}
  playerSymbol="X"
  opponentName="opponent123"
/>
```
