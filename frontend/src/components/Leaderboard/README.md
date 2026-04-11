# Leaderboard Component

**Use case**: UC-12 — View Leaderboard

Tabbed ranking table with game-type selection. Highlights the current player's row and shows an empty state if there are no rows.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `gameTypes` | `string[]` | No | Tab labels (e.g. `["Chess", "Tic-Tac-Toe", "Overall"]`) |
| `selectedGameType` | `string` | No | Active tab |
| `onSelectGameType(type)` | `function` | No | Switch leaderboard view |
| `rankings` | `object[]` | No | API-shaped rows: **`place`** (standings position), **`username`**, **`tier`** (display rank), **`mmr`**, **`wins`**, **`losses`**, **`ties`**. Legacy **`rank`** is accepted as a tier alias. |
| `currentUsername` | `string` | No | Local player's username (highlights their row) |
| `onBack()` | `function` | No | Return to dashboard |

## Usage

```jsx
import Leaderboard from './components/Leaderboard';

<Leaderboard
  gameTypes={['Chess', 'Tic-Tac-Toe', 'Overall']}
  selectedGameType="Chess"
  onSelectGameType={setGameType}
  rankings={[
    { place: 1, username: 'grandmaster', tier: 'Gold', mmr: 1800, wins: 50, losses: 10, ties: 2 },
  ]}
  currentUsername="player1"
  onBack={() => navigate('/dashboard')}
/>
```
