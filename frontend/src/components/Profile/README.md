# Profile Component

**Use case**: UC-09 — View Profile

Displays player info (username, email), overall stats, and per-game stats in a table. Shows a "no games played" message when the player has no history.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `username` | `string` | Yes | Player's username |
| `email` | `string` | Yes | Player's email |
| `generalStats` | `{ gamesPlayed, wins, losses, ties }` | No | Overall stats |
| `gameStats` | `[{ gameType, gamesPlayed, wins, losses, rank, mmr }]` | No | Per-game breakdown |
| `onEditSettings()` | `function` | No | Navigate to account settings |
| `onBack()` | `function` | No | Return to dashboard |

## Usage

```jsx
import Profile from './components/Profile';

<Profile
  username="player1"
  email="player1@example.com"
  generalStats={{ gamesPlayed: 10, wins: 6, losses: 3, ties: 1 }}
  gameStats={[
    { gameType: 'Chess', gamesPlayed: 7, wins: 4, losses: 3, rank: 'Silver', mmr: 1200 },
    { gameType: 'Tic-Tac-Toe', gamesPlayed: 3, wins: 2, losses: 0, rank: 'Gold', mmr: 1400 },
  ]}
  onEditSettings={() => navigate('/settings')}
  onBack={() => navigate('/dashboard')}
/>
```
