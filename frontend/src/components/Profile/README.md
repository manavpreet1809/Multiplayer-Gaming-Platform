# Profile Component

**Use case**: UC-09 — View Profile

Displays player info (username, email), overall stats, and per-game stats in a table. Shows a "no games played" message when the player has no history.

In the real app, **username / email / stats** come from **`AuthContext.user`** when available. Optional **`username`** and **`email`** props provide display fallbacks when context has no user (for example the screenshot strip in `ScreenshotPage`).

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `username` | `string` | No | Display fallback if `AuthContext.user` is missing |
| `email` | `string` | No | Display fallback if `AuthContext.user` is missing |
| `generalStats` | `{ gamesPlayed, wins, losses, ties }` | No | Overall stats (or from `user.stats.overall`) |
| `gameStats` | `[{ gameType, gamesPlayed, wins, losses, ties, rank, mmr }]` | No | Per-game breakdown (or derived from `user.stats.games`, filtered to games with plays) |
| `onEditSettings()` | `function` | No | Navigate to account settings |
| `onBack()` | `function` | No | Return to dashboard |

## Usage

```jsx
import Profile from './components/Profile';
import { AuthContext } from './context/AuthContext';

// Typical: user supplied by AuthProvider
<Profile onEditSettings={() => navigate('/settings')} />

// Storyboard / no auth context: pass display props
<Profile
  username="player1"
  email="player1@example.com"
  generalStats={{ gamesPlayed: 10, wins: 6, losses: 3, ties: 1 }}
  gameStats={[
    { gameType: 'Chess', gamesPlayed: 7, wins: 4, losses: 3, ties: 0, rank: 'Silver', mmr: 1200 },
    { gameType: 'Tic-Tac-Toe', gamesPlayed: 3, wins: 2, losses: 0, ties: 1, rank: 'Gold', mmr: 1400 },
  ]}
  onEditSettings={() => navigate('/settings')}
  onBack={() => navigate('/dashboard')}
/>
```
