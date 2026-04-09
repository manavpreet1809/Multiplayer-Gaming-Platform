# Project status (living notes)

_Last updated: April 2026._

## Client UI (React)

- Full **react-router-dom** navigation: auth flows, dashboard, browse/create/join/matchmake, lobby, game, chat, profile, leaderboard.
- **Screenshot / storyboard mode:** append `?screenshots` to the dev server URL for a long scroll of static UI examples (`ScreenshotPage`).
- **Component tests:** Jest + React Testing Library under `frontend/src` (run `npm test -- --watchAll=false` from `frontend/`).

## Platform core (FastAPI)

- Auth, games REST, WebSockets, and in-memory lobby/game state (see root README for single-worker note).
- **Games / leaderboard API** exposes placement and stats fields consumed by the leaderboard and profile views.

## Integration

- Frontend talks to the API via `REACT_APP_API_URL` (default `http://localhost:8000`). Tokens use **sessionStorage** (see auth service).

## Older notes

### Mar. 17/26

- Client UI had Login; other components existed but were not all wired.
