# Dashboard Component

**Use case**: UC-04 — View Dashboard

Main hub for authenticated players. Displays player status, notifications, and action buttons for all platform features. Status-aware banners highlight when a game is ready, the player is queued, or in a lobby.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `username` | `string` | Yes | Player display name |
| `status` | `"idle" \| "in-lobby" \| "in-queue" \| "game-ready"` | No | Player status (default: `"idle"`) |
| `notifications` | `[{ id, message }]` | No | Pending notifications |
| `onBrowseGames()` | `function` | No | Navigate to game list |
| `onCreateGame()` | `function` | No | Create a new game lobby |
| `onJoinGame()` | `function` | No | Join an existing lobby |
| `onEnqueue()` | `function` | No | Enter matchmaking queue |
| `onOpenChat()` | `function` | No | Open chat panel |
| `onJoinActiveGame()` | `function` | No | Join a ready game session |
| `onViewProfile()` | `function` | No | Navigate to profile |
| `onLeaderboard()` | `function` | No | Navigate to leaderboard |
| `onLogout()` | `function` | No | Log out |

## Usage

```jsx
import Dashboard from './components/Dashboard';

<Dashboard
  username="player1"
  status="idle"
  notifications={[]}
  onBrowseGames={() => navigate('/games')}
  onCreateGame={() => createLobby()}
  onJoinGame={() => navigate('/join')}
  onLogout={() => logout()}
/>
```
