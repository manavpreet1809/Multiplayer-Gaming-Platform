# GameList Component

**Use case**: UC-01 — View Game List

Displays available games as a card grid. Selecting a card shows a detail panel with a "Join Lobby" button. Shows an empty-state message when no games are available.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `games` | `[{ id, name, description, playerCount }]` | No | Available games (default: `[]`) |
| `selectedGameId` | `string \| null` | No | Currently selected game |
| `onSelectGame(id)` | `function` | No | Called when a game card is clicked |
| `onJoinLobby(id)` | `function` | No | Called when "Join Lobby" is clicked |
| `onBack()` | `function` | No | Return to previous view |

## Usage

```jsx
import GameList from './components/GameList';

const games = [
  { id: 'chess', name: 'Chess', description: 'Classic chess', playerCount: 42 },
  { id: 'ttt', name: 'Tic-Tac-Toe', description: 'Classic 3x3', playerCount: 18 },
];

<GameList
  games={games}
  selectedGameId={selected}
  onSelectGame={setSelected}
  onJoinLobby={(id) => joinLobby(id)}
  onBack={() => navigate('/dashboard')}
/>
```
