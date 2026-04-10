# GameLobby Component

**Use case**: UC-05 — Join Game Lobby

Pre-game waiting room showing players, ready states, and empty slots. Supports an embedded Chat component via the `chatComponent` prop.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `lobbyId` | `string` | Yes | Unique lobby identifier |
| `gameName` | `string` | Yes | Name of the game |
| `status` | `"waiting" \| "started"` | No | Lobby status (default: `"waiting"`) |
| `players` | `[{ id, username, isReady }]` | No | Current players |
| `requiredPlayers` | `number` | No | Players needed to start (default: `2`) |
| `onLeaveLobby()` | `function` | No | Leave the lobby |
| `onToggleReady()` | `function` | No | Toggle ready status |
| `onStartGame()` | `function` | No | Start the game (leader only, shown when lobby is full) |
| `chatComponent` | `React.Node` | No | Embedded chat panel |

## Usage

```jsx
import GameLobby from './components/GameLobby';
import Chat from './components/Chat';

<GameLobby
  lobbyId="abc123"
  gameName="Chess"
  status="waiting"
  players={[{ id: '1', username: 'player1', isReady: true }]}
  requiredPlayers={2}
  onLeaveLobby={() => leaveLobby()}
  onToggleReady={() => toggleReady()}
  chatComponent={<Chat messages={msgs} onSendMessage={send} context="lobby" />}
/>
```
