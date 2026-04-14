# Iteration 3 video guide — what to show and say

This document turns the course **Product Showcase** and **Individual Technical Demo** requirements into a shot list and talking points for your team. It matches this repo: FastAPI backend, React frontend, MongoDB, local-only deployment.

**Related docs**

- [Local deployment and video capture](LOCAL_DEPLOYMENT_AND_VIDEO.md)
- [Root README](../README.md) (build and run)

---

## Product showcase video (group)

**Length:** maximum 15 minutes.

**Goal:** Show what the platform does from a **user’s perspective**. Avoid deep code walkthroughs.

**Deliverables:** Follow course upload rules. Include a plain-text **`timestamps.txt`** with section start times (example: `0:00 Intro`, `1:45 Setup`).

### Time budget overview

| Approx. time | Section |
|--------------|---------|
| 0:00 - 2:00 | Team introduction |
| 2:00 - 3:00 | Setup and execution |
| 3:00 - 5:00 | Multiplayer interface |
| 5:00 - 7:00 | Matchmaking and lobby |
| 7:00 - 8:00 | Stubbed network and database |
| 8:00 - 9:00 | Sample games |
| 9:00 - 11:00 | Design changes and integration |
| 11:00 - 13:00 | Test execution |
| 13:00 - 15:00 | Buffer or optional extras |

---

### 1. Team introduction (about 1-2 minutes)

**On screen**

- Title slide or app home screen; optional names and roles.

**Say**

- Who is on the team, course/section, product name.
- One sentence each on what each subgroup owned (examples: auth, games, UI).

---

### 2. Setup and execution (about 1 minute)

**On screen**

- Terminal (optional: MongoDB running), backend start, frontend start.

**Say**

- Follow the **README**: Python venv, `pip install`, Uvicorn at `127.0.0.1:8000`, `npm start` at `localhost:3000`.
- Root **`.env`** and **`SECRET_KEY`** are required; do not read secrets aloud.
- If you mention lobbies or live games: **one Uvicorn worker** so in-memory state stays consistent.

---

### 3. Multiplayer interface (about 2 minutes)

**On screen**

- **Two browser windows**, or two dev ports (example: `3000` and `3002`), each logged in as a **different user**.

**Say**

- Different origins mean separate storage, so two real sessions.
- Walk through something that proves two identities (dashboard, profile, or in-game sides).

---

### 4. Matchmaking and lobby (about 2 minutes)

**On screen**

- Create game, join by code or list, matchmaking if you have it; then both players in the same live game.

**Say**

- Happy path: host creates, second player joins, **both see the same game state**.
- If any part is stubbed, say clearly what is **real** versus **simulated**.

---

### 5. Stubbed network and database (about 1 minute)

**On screen**

- Split: OpenAPI docs at `/docs` or browser Network tab **and** MongoDB Compass or a quick peek at persisted data (example: `users`).

**Say**

- **Database:** what you persist (users, auth-related fields, stats, etc.).
- **Networking:** WebSockets or HTTP to **your** local server; what would change if hosted online; you are **not** required to deploy publicly.

---

### 6. Sample games (about 1 minute)

**On screen**

- Short clip **per** shipped game type (example: chess move, tic-tac-toe finished game).

**Say**

- One clear **win** or **draw** so rules are visible. Keep it short.

---

### 7. Design changes and integration challenges (about 2 minutes)

**On screen**

- A diagram from `design.zip`, or a simple sketch: browser to API to Mongo, WebSocket arrow if you use it.

**Say**

- Two or three **concrete** integration stories (examples: CORS and multiple dev ports, auth tokens, game state vs lobby state, merge pain).
- Focus on **how you integrated**, not blame.

---

### 8. Test execution (about 2 minutes)

**On screen**

- Terminal: backend `pytest`, frontend `npm test` (non-interactive, not watch mode).

**Say**

- Show **passing** runs.
- Summarize **what** is covered (API, game logic, UI components). Optional: `CI=true npm run build` if you use it.

---

### 9. Buffer / optional depth (remaining time)

**On screen**

- Extra feature: chat, leaderboard, profile, etc.

**Say**

- Only if time allows. Prefer clear audio and a polished flow over cramming.

---

### Showcase checklist before recording

- [ ] MongoDB running; backend and frontend up; avoid Safari (per README).
- [ ] Two test accounts ready; flows rehearsed once.
- [ ] API docs: `http://127.0.0.1:8000/docs`
- [ ] Large terminal font for readability on video.
- [ ] `timestamps.txt` matches the **final** edited video.

---

## Individual technical demo

**Length:** maximum 10 minutes.

**Goal:** Show **your** contribution and that you **understand** it. Do not only read code line by line.

### Opening (about 30 seconds)

- Your name and team.
- Subgroups you were on and your roles (examples: REST and Mongo for games, React board and WebSocket client).

### Main body (about 8-9 minutes)

Pick **one or two** features you actually built. For **each** feature, cover:

1. **Problem** — What user or system need does this address?
2. **Where it lives** — Short pointer to files or modules; one diagram or route list is enough.
3. **Walkthrough** — One request or one user action, end to end (browser to API to database or WebSocket).
4. **Why this design** — Use the depth checklist below (two or three points per important block).
5. **Tests** — What you ran or wrote; what fails if this breaks.

### Depth checklist (markers want 2-3 of these per significant block)

Use while pointing at **real** code:

- **Alternatives** — Why this approach instead of another (example: FastAPI dependencies vs one huge module; `sessionStorage` vs `localStorage` for tokens).
- **If removed** — Example: skipping normalization makes profile and leaderboard disagree; wrong CORS blocks the second browser.
- **Domain meaning** — Example: `game_id` is the lobby key; `player_ids` match authenticated users.
- **Assumptions** — Example: single worker; Mongo unique username index.
- **Testing** — Example: pytest for API; Jest with mocked `fetch`.
- **Architecture** — Example: who calls this; what updates when a game ends.

### What to avoid

- Saying only “it calls method X then Y” with no **why** and no **failure mode**.
- More than **two** deep dives unless you are very fast.
- Secrets, real passwords, or personal emails (use demo accounts).

### Deliverables

- **`tech_demo_link.txt`** or **`tech_demo.mp4`** per course instructions.
- Timestamp file as required (section starts in plain text).

---

## Timestamps file (`timestamps.txt`)

Align times with the **final** uploaded cut. Example:

```text
0:00 - Title / team intro
1:30 - Environment setup and run instructions
3:00 - Two-player / multiplayer UI
```

---

## Cross-reference to course rubric

| Course asks for | Where in this guide |
|-----------------|---------------------|
| Group: user perspective | Sections 1-6 (flows before tests) |
| Group: tests on screen | Section 8 |
| Individual: contribution and integration | Main body + walkthrough |
| Individual: real explanation, not narration | Depth checklist |
| Optional: DB / network | Section 5 |

If your TA gave a stricter template, follow that first; use this document for **content** only.
