# OMG Platform — Frontend

React-based client UI for the OMG gaming platform. Supports **Chess** and **Tic-Tac-Toe**.

## Quick Start

```bash
cd frontend
npm install
npm start        # dev server at http://localhost:3000
npm test         # interactive watch mode; CI-style once: npm test -- --watchAll=false
npm run build    # production build → build/
```

Optional **`frontend/.env`**:

```bash
# Defaults to http://localhost:8000 if omitted
REACT_APP_API_URL=http://127.0.0.1:8000
```

Restart the dev server after changing env files.

## Tech Stack

- **React 19** (Create React App)
- **react-router-dom** v7 (in-app routing)
- **Roboto** font (Google Fonts, loaded globally)
- **Plain CSS** (component-scoped, no framework)
- **Jest + React Testing Library** for tests (see `setupTests.js` and `package.json` `jest` keys for React Router / `TextEncoder` compatibility)

## Project Structure

```
frontend/src/
├── components/             Feature folders (each with .js, .css, tests, often index.js)
│   ├── Login, Register, ResetPassword, Dashboard, GameList, GameLobby, Chat, …
│   ├── *Page/              Routed pages (e.g. DashboardPage, LobbyPage, GamePage)
│   ├── ChessBoard/, TicTacToeBoard/, GameBoardDemo/, ErrorBoundary/, …
├── context/                AuthContext (+ tests)
├── services/               authService, gameService (+ __mocks__/gameService.js for Jest)
├── test/                   renderWithAuth / renderWithRouter helpers
├── adapters/               game state → board props
├── App.js                  Routes, protected routes, screenshot mode (?screenshots)
├── ScreenshotPage.js       Long UI strip for captures / design review
├── index.js                Entry (BrowserRouter + AuthProvider)
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

Most presentational components are **props-driven shells** (no embedded API calls). **`App.js`**, **`*Page` components**, and **`AuthContext`** own routing, auth session, and service calls. Board and lobby pieces stay visual / callback-driven for clarity.

### Conditional Rendering

Optional features (nav links, action buttons) only render when their corresponding callback prop is provided. This makes components reusable across different contexts.

### Consistent Styling

- **Font**: Roboto (300/400/500/700 weights), set on `body` in `index.css` and explicitly on form elements (`<input>`, `<button>`) which don't inherit by default
- **Color palette**:
  - `#662691` (purple) — primary buttons, links, headings
  - `#BEB8EB` (lavender) — borders, secondary surfaces
  - `#F56476` (coral) — errors, danger, logout
  - `#ADFCF9` (mint) — success, ready, info
  - `#F8F4A6` (yellow) — warnings, notifications, highlights
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

Reads **`AuthContext.user`** for username, email, and nested stats when used in the real app. Optional props override display when context has no user (e.g. **`ScreenshotPage`**).

| Prop | Type | Description |
|------|------|-------------|
| `username` | `string` | Optional display fallback if `user` missing in context |
| `email` | `string` | Optional display fallback if `user` missing in context |
| `generalStats` | `{ gamesPlayed, wins, losses, ties }` | Overall stats (props or inferred from `user.stats.overall`) |
| `gameStats` | `[{ gameType, gamesPlayed, wins, losses, ties?, rank, mmr }]` | Per-game stats (props or inferred from `user.stats.games`) |
| `onEditSettings()` | `function` | Navigate to account settings |
| `onBack()` | `function` | Return to dashboard |

**Features**: Info card, stat grid, per-game stats table (only games with `gamesPlayed > 0`), "no games played" state.

---

#### Leaderboard

**Use case**: UC-12 — View Leaderboard

| Prop | Type | Description |
|------|------|-------------|
| `gameTypes` | `string[]` | Available game type tabs (e.g. `["Chess", "Tic-Tac-Toe", "Overall"]`) |
| `selectedGameType` | `string` | Active tab |
| `onSelectGameType(type)` | `function` | Switch leaderboard |
| `rankings` | `[{ place, username, tier, mmr, wins, losses, ties?, rank? }]` | Rows from API: **`place`** is standings position; legacy **`rank`** may mean tier only |
| `currentUsername` | `string` | Local player (to highlight their row) |
| `onBack()` | `function` | Return to dashboard |

**Features**: Game-type tabs, table columns `#` / W-L-T, current-player highlight, empty state when no rankings.

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

## Integration notes

1. **Routing**: `BrowserRouter` and routes live in `index.js` / `App.js`. Use `MemoryRouter` in tests (`renderWithAuth` in `src/test/testUtils.js`).
2. **Auth**: `AuthProvider` + `sessionStorage`-backed tokens in `services/authService.js`.
3. **Games**: `services/gameService.js` (REST + WebSocket helpers) — Jest uses `src/services/__mocks__/gameService.js` so partial mocks do not break other tests.
4. **Game logic**: Board components render state and forward clicks; validation and engine rules stay on the server.
