# GameResults Component

**Use case**: UC-14 — View Game Results

Post-game results screen with a color-coded outcome banner (win/loss/draw), MMR change, rank update, and action buttons.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `result` | `"win" \| "loss" \| "draw"` | Yes | Game outcome |
| `winnerUsername` | `string \| null` | No | Winner's name (null for draw) |
| `mmrChange` | `number` | No | MMR gained or lost |
| `newRank` | `string \| null` | No | Updated rank (if changed) |
| `onReturnDashboard()` | `function` | No | Navigate to dashboard |
| `onPlayAgain()` | `function` | No | Re-queue for same game type |
| `onViewLeaderboard()` | `function` | No | Navigate to leaderboard |

## Usage

```jsx
import GameResults from './components/GameResults';

<GameResults
  result="win"
  winnerUsername="player1"
  mmrChange={25}
  newRank="Gold"
  onReturnDashboard={() => navigate('/dashboard')}
  onPlayAgain={() => enqueue('chess')}
  onViewLeaderboard={() => navigate('/leaderboard')}
/>
```
