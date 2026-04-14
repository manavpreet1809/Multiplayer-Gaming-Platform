# Local deployment and video capture

This guide is for anyone who needs a **working local build** on their machine—for development, demos, or **course video segments**. Follow it in order the first time; later you can skip steps you have already done.

For the shortest path, the [root README](../README.md) “Run the Project Locally” section matches these steps. This document adds **video-specific tips**, **environment variables**, and **verification commands**.

---

## 1. What you need installed

| Tool | Notes |
|------|--------|
| **Python 3.11+** | Backend (FastAPI). Check: `python --version` or `py -3.11 --version` (Windows). |
| **Node.js 20+** | Frontend toolchain; React Router v7 expects Node 20+. Check: `node -v`. |
| **npm** | Comes with Node (`npm -v`). |
| **MongoDB** | Local instance on port `27017` (default). Use the root README for OS-specific `mongod` commands. |
| **Git** | To clone and pull the repo. |

**Browsers:** Use **Chrome**, **Firefox**, or **Edge** for recording. The team README states **do not use Safari** for this project.

---

## 2. One-time setup (per machine)

### 2.1 Clone and enter the repo

```bash
git clone <repository-url>
cd seng300-202601-pg-3
```

### 2.2 Backend environment file

Create **`.env` in the repository root** (same folder as `requirements.txt`). Minimum:

```bash
# Required — generate with:
#   python3 -c "import secrets; print(secrets.token_hex(32))"
#   Windows: py -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=<paste-a-long-random-hex-string-here>

MONGODB_URL=mongodb://localhost:27017
DB_NAME=myapp

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Never commit `.env`.

### 2.3 Python virtual environment and packages

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2.4 Frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 2.5 Optional: point the UI at a non-default API

By default the React app calls `http://localhost:8000`. To override (e.g. another port or host), create **`frontend/.env`**:

```bash
REACT_APP_API_URL=http://127.0.0.1:8000
```

Restart `npm start` after changing this file.

---

## 3. Running the stack every day

You need **MongoDB**, the **backend**, and the **frontend** running at the same time. Use **three terminals** (or the helper script).

### 3.1 Terminal A — MongoDB

If MongoDB is not already running as a service, start `mongod` with a data directory (see root README §2.6).

### 3.2 Terminal B — Backend

From the **repo root**, with the venv activated:

**macOS / Linux**

```bash
export PYTHONPATH=src
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = 'src'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check: [http://localhost:8000/docs](http://localhost:8000/docs)

Use a **single** Uvicorn worker for local dev (default); restarting the backend clears in-memory lobbies and games.

### 3.3 Terminal C — Frontend

```bash
cd frontend
npm start
```

Open: [http://localhost:3000](http://localhost:3000)

### 3.4 Optional: one-shot script

From repo root:

- **macOS / Linux:** `./scripts/dev-macos.sh`
- **Windows:** `.\scripts\dev-windows.ps1`

If MongoDB is already running: `SKIP_MONGO=1` (macOS) or `$env:SKIP_MONGO='1'` (Windows) before the script. See root README §2.5.

---

## 4. Production build (optional)

Useful if you need a static bundle or to verify the app builds cleanly before recording.

```bash
cd frontend
npm run build
```

Output: `frontend/build/`. The usual workflow for this course is still **`npm start`** against a live backend for demos.

---

## 5. Verification before recording

Run these from the repo so you can show “tests pass” in video or confirm your machine is good.

**Backend (repo root, venv on)**

```bash
pytest src/app/test -q
```

**Frontend**

```bash
cd frontend
npm test -- --watchAll=false
```

On Windows PowerShell you can set `$env:CI='true'` before `npm test` so Jest exits after one run.

---

## 6. Video and demo tips

### 6.1 Multiplayer / lobby footage

- Run the **backend + DB + frontend** as above.
- Use **two browser profiles** (or one normal window + one private window) and **two registered accounts** to show two players in a lobby or game.
- If something looks stuck, confirm both tabs can reach `http://localhost:8000/docs` and that the frontend URL matches your `REACT_APP_API_URL` if you set it.

### 6.2 UI-only screenshot strip (no login)

To scroll through static UI examples (login, dashboard, boards, etc.) without navigating the real app, open:

```text
http://localhost:3000/?screenshots
```

The query parameter must be **`screenshots`**. Useful for B-roll or design walkthroughs.

### 6.3 Recording quality

- Fullscreen the browser or use a fixed viewport so resolution stays consistent across takes.
- Close unrelated apps to reduce fan noise and CPU spikes during screen capture.

### 6.4 Segment ownership

See [videoplanningdoc.md](./videoplanningdoc.md) for who covers which topic in the submission video; each presenter still uses this same local setup.

---

## 7. Common issues

| Symptom | What to check |
|--------|----------------|
| `SECRET_KEY` error | Root `.env` exists and `SECRET_KEY` is non-empty. |
| MongoDB connection errors | `mongod` running; `MONGODB_URL` in root `.env`. |
| Frontend cannot reach API | Backend on port 8000; `frontend/.env` `REACT_APP_API_URL` if non-default. |
| `uvicorn` not found | Activate `.venv` first, or `python -m uvicorn ...`. |
| Port 3000 busy | Accept CRA’s alternate port or set `PORT` (see root README). |
| Blank or failing tests | Run `npm install` in `frontend/`; use Node 20+. |

For more detail, see the **[root README](../README.md)** (full macOS/Windows walkthroughs and troubleshooting).
