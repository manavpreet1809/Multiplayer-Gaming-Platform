# OMG Platform — Frontend

React-based client UI for the OMG gaming platform. Supports **Chess** and **Tic-Tac-Toe**.

## Quick Start

```bash
cd frontend
npm install
npm start        # dev server at http://localhost:3000
npm test         # run all tests
npm run build    # production build
```

## Tech Stack

- **React 19** (Create React App)
- **Roboto** font (Google Fonts, loaded globally)
- **Plain CSS** (component-scoped, no framework)
- **Jest + React Testing Library** for tests

## Project Structure

```
frontend/src/
├── components/
│   ├── Login/              AUTH-02 / UC-03 — Log in form
│   ├── Register/           AUTH-01 / UC-02 — Account registration form
│   ├── ResetPassword/      AUTH-03        — Password reset flow
│   ├── Dashboard/          UC-04          — Authenticated landing page
│   ├── GameList/           UC-01          — Browse available games
│   ├── GameLobby/          UC-05          — Pre-game waiting room
│   ├── Chat/               UC-07          — Chat messages panel
│   ├── Profile/            UC-09          — Player stats and info
│   ├── Leaderboard/        UC-12          — Rankings table
│   ├── GameResults/        UC-14          — Post-game results screen
│   ├── ChessBoard/         UC-13 UI       — Chess board visual component
│   └── TicTacToeBoard/     UC-13 UI       — Tic-Tac-Toe board visual component
├── App.js                  Root component
├── App.css
├── index.js                Entry point
└── index.css               Global styles (Roboto import)
```

Each component follows the same structure:

```
ComponentName/
├── ComponentName.js        Component source
├── ComponentName.css       Scoped styles
├── ComponentName.test.js   Tests (where applicable)
└── index.js                Barrel export
```

## Design Principles

### Props-Driven / No Baked-In Logic

All components are **UI shells**. They receive data and callbacks via props and contain no routing, authentication, or game logic. This allows the backend team to wire them up with any state management or routing solution.

### Conditional Rendering

Optional features (nav links, action buttons) only render when their corresponding callback prop is provided. This makes components reusable across different contexts.

### Consistent Styling

- **Font**: Roboto (300/400/500/700 weights), set on `body` in `index.css` and explicitly on form elements (`<input>`, `<button>`) which don't inherit by default
- **Color palette**: Primary blue `#1976d2`, error red `#b71c1c`, success green `#2e7d32`
- **Layout**: Centered card forms for auth flows; max-width containers for dashboard views

---

## Component Reference

### Authentication Components

#### Login

**Use case**: AUTH-02 / UC-03 — Log In

| Prop | Type | Description |
|------|------|-------------|
| `onLogin(identifier, password)` | `function → Promise` | Called on submit; resolve = success, reject = show error |
| `onForgotPassword()` | `function` | Navigate to reset password view |
| `onRegister()` | `function` | Navigate to registration view |

**Features**: Client-side empty-field validation, loading state, generic error display.

---

#### Register

**Use case**: AUTH-01 / UC-02 — Create Account

| Prop | Type | Description |
|------|------|-------------|
| `onRegister(username, email, password)` | `function → Promise` | Called on submit |
| `onLogin()` | `function` | Navigate to login view |

**Features**: Username + email + password + confirm-password fields, min 6-char password validation, duplicate-password check.

---

#### ResetPassword

**Use case**: AUTH-03 — Reset Password

| Prop | Type | Description |
|------|------|-------------|
| `onResetPassword(identifier, newPassword)` | `function → Promise` | Called on reset submit |
| `onBackToLogin()` | `function` | Navigate back to login |

**Features**: Two-step flow (identify → reset), password validation, success confirmation.

---

### Platform Components

#### Dashboard

**Use case**: UC-04 — View Dashboard

| Prop | Type | Description |
|------|------|-------------|
| `username` | `string` | Display name |
| `status` | `"idle" \| "in-lobby" \| "in-queue" \| "game-ready"` | Player status |
| `notifications` | `[{ id, message }]` | Notification list |
| `onBrowseGames()` | `function` | Navigate to game list |
| `onCreateGame()` | `function` | Create a new game lobby |
| `onJoinGame()` | `function` | Join an existing game lobby |
| `onEnqueue()` | `function` | Enter matchmaking queue |
| `onOpenChat()` | `function` | Open chat panel |
| `onJoinActiveGame()` | `function` | Join a ready game session |
| `onViewProfile()` | `function` | Navigate to profile |
| `onLeaderboard()` | `function` | Navigate to leaderboard |
| `onLogout()` | `function` | Log out |

**Features**: Status-aware banners (game ready, in queue, in lobby), notification section, action grid.

---

#### GameList

**Use case**: UC-01 — View Game List

| Prop | Type | Description |
|------|------|-------------|
| `games` | `[{ id, name, description, playerCount }]` | Available games |
| `selectedGameId` | `string \| null` | Currently selected game |
| `onSelectGame(id)` | `function` | Select a game card |
| `onJoinLobby(id)` | `function` | Join lobby for selected game |
| `onBack()` | `function` | Return to previous view |

**Features**: Card grid, detail panel on selection, empty state message.

---

#### GameLobby

**Use case**: UC-05 — Join Game Lobby

| Prop | Type | Description |
|------|------|-------------|
| `lobbyId` | `string` | Lobby identifier |
| `gameName` | `string` | Name of the game |
| `status` | `"waiting" \| "started"` | Lobby status |
| `players` | `[{ id, username, isReady }]` | Current players |
| `requiredPlayers` | `number` | Players needed to start (default: 2) |
| `onLeaveLobby()` | `function` | Leave the lobby |
| `onToggleReady()` | `function` | Toggle ready status |
| `onStartGame()` | `function` | Start the game (leader only) |
| `chatComponent` | `React.Node` | Embedded Chat component |

**Features**: Player list with ready indicators, empty slots, start button when full.

---

#### Chat

**Use case**: UC-07 — Chat

| Prop | Type | Description |
|------|------|-------------|
| `messages` | `[{ id, sender, text, timestamp }]` | Chat messages |
| `onSendMessage(text)` | `function` | Send a message |
| `context` | `"lobby" \| "global"` | Chat context label (default: `"global"`) |

**Features**: Scrollable message list, input form, empty-message prevention.

---

#### Profile

**Use case**: UC-09 — View Profile

| Prop | Type | Description |
|------|------|-------------|
| `username` | `string` | Player's username |
| `email` | `string` | Player's email |
| `generalStats` | `{ gamesPlayed, wins, losses, ties }` | Overall stats |
| `gameStats` | `[{ gameType, gamesPlayed, wins, losses, rank, mmr }]` | Per-game stats |
| `onEditSettings()` | `function` | Navigate to account settings |
| `onBack()` | `function` | Return to dashboard |

**Features**: Info card, stat grid, per-game stats table, "no games played" state.

---

#### Leaderboard

**Use case**: UC-12 — View Leaderboard

| Prop | Type | Description |
|------|------|-------------|
| `gameTypes` | `string[]` | Available game type tabs (e.g. `["Chess", "Tic-Tac-Toe", "Overall"]`) |
| `selectedGameType` | `string` | Active tab |
| `onSelectGameType(type)` | `function` | Switch leaderboard |
| `rankings` | `[{ rank, username, tier, mmr, wins, losses }]` | Leaderboard entries |
| `currentUsername` | `string` | Local player (to highlight their row) |
| `onBack()` | `function` | Return to dashboard |

**Features**: Game-type tabs, ranking table, current-player highlight, unranked message.

---

#### GameResults

**Use case**: UC-14 — View Game Results

| Prop | Type | Description |
|------|------|-------------|
| `result` | `"win" \| "loss" \| "draw"` | Game outcome |
| `winnerUsername` | `string \| null` | Winner's name |
| `mmrChange` | `number` | MMR gained or lost |
| `newRank` | `string \| null` | Updated rank (if changed) |
| `onReturnDashboard()` | `function` | Go to dashboard |
| `onPlayAgain()` | `function` | Re-queue for same game |
| `onViewLeaderboard()` | `function` | Go to leaderboard |

**Features**: Color-coded result banner, MMR delta display, action buttons.

---

### Game Board Components

#### ChessBoard

**Use case**: UC-13 UI — Submit Move (visual only)

| Prop | Type | Description |
|------|------|-------------|
| `board` | `string[][] (8x8)` | Piece codes: uppercase = white (`K Q R B N P`), lowercase = black (`k q r b n p`), `null` = empty. Row 0 = rank 8. |
| `selectedSquare` | `{ row, col }` | Currently selected square |
| `highlightedSquares` | `[{ row, col }]` | Legal move indicators |
| `lastMove` | `{ from: {row,col}, to: {row,col} }` | Last move highlight |
| `currentPlayer` | `"white" \| "black"` | Whose turn |
| `isMyTurn` | `boolean` | Whether local player can interact |
| `onSquareClick(row, col)` | `function` | Square click handler |
| `playerColor` | `"white" \| "black"` | Local player's color (flips board) |
| `opponentName` | `string` | Opponent display name |
| `capturedByWhite` | `string[]` | Pieces captured by white |
| `capturedByBlack` | `string[]` | Pieces captured by black |

**Features**: Unicode chess pieces (no images), file/rank labels, board flipping, move dots, capture rings, last-move highlight, captured-pieces tray, responsive layout.

Renders the default starting position when no `board` prop is provided.

---

#### TicTacToeBoard

**Use case**: UC-13 UI — Submit Move (visual only)

| Prop | Type | Description |
|------|------|-------------|
| `board` | `("X" \| "O" \| null)[]` | Flat array of 9 cells |
| `winningCells` | `number[]` | Indices of winning line (e.g. `[0,1,2]`) |
| `currentPlayer` | `"X" \| "O"` | Whose turn |
| `isMyTurn` | `boolean` | Whether local player can interact |
| `onCellClick(index)` | `function` | Cell click handler |
| `playerSymbol` | `"X" \| "O"` | Local player's mark |
| `opponentName` | `string` | Opponent display name |

**Features**: 3x3 CSS Grid board, X/O color coding (blue/red), winning-cell highlight, turn indicator, disabled cells when not your turn.

---

## Integration Notes

These components are designed to be wired up by the backend/integration team:

1. **Routing**: No router is installed yet. Add `react-router-dom` and map components to routes.
2. **State management**: Components are stateless (aside from form inputs). Add Context, Redux, or similar to manage auth sessions and game state.
3. **API calls**: Pass async functions as callback props (e.g., `onLogin` should call the auth API and throw on failure).
4. **Game logic**: Board components only render state and forward clicks. Move validation, turn management, and win detection belong in the backend / game engine layer.
