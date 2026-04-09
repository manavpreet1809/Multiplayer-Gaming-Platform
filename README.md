## Tech Stack

- Database: MongoDB
- Backend: FastAPI (Python)
- Frontend: React.js (JavaScript)

---

## 1. Required Software

### macOS

- **Python 3.11+** — `python3 --version`. Install via [python.org](https://www.python.org/downloads/) or `brew install python@3.11`.
- **Node.js 18+** — `node -v`. Install via [nodejs.org](https://nodejs.org/) or `brew install node`.
- **npm** — Ships with Node.js (`npm -v`).
- **MongoDB** — Local server for development. Easiest: use a data folder under your home directory and `--dbpath` (see **Run the Project** → **macOS**). [Homebrew](https://brew.sh/) is optional.
- **MongoDB Compass** (optional) — Download the macOS `.dmg` from [MongoDB Compass](https://www.mongodb.com/products/compass).

### Windows

- **Python 3.11+** — Install from [python.org](https://www.python.org/downloads/) and ensure **Add Python to PATH** is checked, or use the Microsoft Store / `winget install Python.Python.3.11`.
- **Node.js 18+** — Install the LTS installer from [nodejs.org](https://nodejs.org/) (includes npm).
- **MongoDB** — Install [MongoDB Community Server](https://www.mongodb.com/try/download/community) for Windows, or use WSL2 and follow the Linux/Homebrew flow if you prefer.
- **MongoDB Compass** (optional) — Windows installer from [MongoDB Compass](https://www.mongodb.com/products/compass).
- **Terminal** — Use **PowerShell**, **Command Prompt**, or **Windows Terminal** for the commands below.

---

## 2. Run the Project

Use the section for your OS. All paths assume the **repository root** (the folder that contains `frontend/`, `src/`, and `requirements.txt`).

**Quick start (optional):** from the repo root, **macOS** can run `./scripts/dev-macos.sh` (starts MongoDB if port 27017 is free, then uvicorn, then `npm start` in the foreground). **Windows (PowerShell):** `.\scripts\dev-windows.ps1`. Requires existing `.venv` and dependencies; set `SKIP_MONGO=1` if MongoDB is already running. Override the data directory with `MONGO_DATA` if needed.

### macOS

```bash
cd "/path/to/seng300-202601-pg-3"
```

#### Backend (FastAPI)

1. **Virtual environment (recommended)**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **MongoDB**

   **Option A — Data directory in your home folder (recommended)**

   Plain `mongod` with no arguments uses `/data/db`, which does not exist on macOS by default. Use a folder you own:

   ```bash
   mkdir -p ~/mongodb-data
   mongod --dbpath ~/mongodb-data
   ```

   **Important:** Creating `~/mongodb-data` does not switch MongoDB away from `/data/db`. You must start the server with **`mongod --dbpath ~/mongodb-data`** every time. Running plain `mongod` will always look for `/data/db` and fail on macOS unless you created that path.

   Leave that terminal open while you develop. To stop MongoDB, press Ctrl+C in that window.

   **Option B — Homebrew service**

   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb-community
   ```

   Stop later with: `brew services stop mongodb-community`.

   **Option C — Homebrew `mongod` with its config (second terminal)**

   ```bash
   mongod --config "$(brew --prefix)/etc/mongod.conf"
   ```

   (Apple Silicon: Homebrew is often under `/opt/homebrew`; Intel Macs: `/usr/local`.)

4. **Environment file** — Create `.env` in the **project root** (see [Shared `.env` contents](#shared-env-contents) below).

5. **Start the backend** (venv activated, from project root). The app imports `app.*`, so `src` must be on `PYTHONPATH`:

   ```bash
   PYTHONPATH=src uvicorn app.main:app --reload
   ```

   - API: [http://localhost:8000](http://localhost:8000)  
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Frontend (React)

Open another terminal tab/window.

```bash
cd frontend
npm install    # or: yarn
npm start      # or: yarn start
```

- App: [http://localhost:3000](http://localhost:3000)

---

### Windows

```powershell
cd C:\path\to\seng300-202601-pg-3
```

#### Backend (FastAPI)

1. **Virtual environment (recommended)**

   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   ```

   If `py` is not available, use `python -m venv .venv` and the same `activate` line.

2. **Install Python dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

3. **MongoDB**

   - Install MongoDB Community and add the **bin** folder to your **PATH**, **or** run `mongod.exe` from the install directory (version varies), for example:

   ```powershell
   cd "C:\Program Files\MongoDB\Server\8.2\bin"
   .\mongod.exe
   ```

   Keep that window open, or install MongoDB as a **Windows Service** so it starts automatically.

4. **Environment file** — Create `.env` in the **project root** (see [Shared `.env` contents](#shared-env-contents) below).

5. **Start the backend** (venv activated, from project root). The app imports `app.*`, so `src` must be on `PYTHONPATH`:

   ```powershell
   $env:PYTHONPATH = "src"
   uvicorn app.main:app --reload
   ```

   - API: [http://localhost:8000](http://localhost:8000)  
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Frontend (React)

Open a second terminal.

```powershell
cd frontend
npm install    # or: yarn
npm start      # or: yarn start
```

- App: [http://localhost:3000](http://localhost:3000)

---

### Shared `.env` contents

Create a file named `.env` in the **project root** with:

```bash
# Generate SECRET_KEY with:
# python3 -c "import secrets; print(secrets.token_hex(32))"
#   (Windows: py -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=

# MongoDB
MONGODB_URL=mongodb://localhost:27017
DB_NAME=myapp

# Token expiry
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> **Important:** Set a real `SECRET_KEY` before starting the app. Do not commit `.env`.

---

## 3. Build the App

Production build steps are the same for the frontend on both platforms; only the way you open a terminal and `cd` into the repo differs.

### macOS

From the repository root:

```bash
cd frontend
npm install
npm run build
```

Output: `frontend/build/`.

### Windows

From the repository root:

```powershell
cd frontend
npm install
npm run build
```

Output: `frontend/build/`.

### Backend

There is no separate compile step; the FastAPI app runs with Python/Uvicorn. For deployment, install dependencies on the server and run the same command with `PYTHONPATH=src` (or set `PYTHONPATH` in the service environment).

---

## 4. Expected Result

- Login page loads in the browser at [http://localhost:3000](http://localhost:3000).
- Backend API responds; routes may be stubbed if the database is not fully connected.
- FastAPI docs are available at `/docs` on the backend port.

---

## 5. Common Problems

### macOS

- **Port already in use** — Stop the other app or use `PORT=3001 npm start` for React.
- **MongoDB connection refused** — Ensure `mongod` is running (`mongod --dbpath ~/mongodb-data` in a terminal, or `brew services list` if you use Homebrew). Confirm `MONGODB_URL` in `.env`.
- **`NonExistentPath: Data directory /data/db not found`** — You ran `mongod` without `--dbpath`. Create a folder and use it: `mkdir -p ~/mongodb-data` then `mongod --dbpath ~/mongodb-data`.
- **`uvicorn: command not found`** — Activate the venv (`source .venv/bin/activate`) or run `PYTHONPATH=src python3 -m uvicorn app.main:app --reload`.

### Windows

- **Port already in use** — Another app uses `3000` or `8000`. Close it or set `set PORT=3001` then `npm start` (CMD) or `$env:PORT=3001` (PowerShell).
- **MongoDB connection refused** — Ensure `mongod` is running (service or dedicated terminal); confirm `MONGODB_URL` in `.env`.
- **`uvicorn` is not recognized** — Activate `.venv\Scripts\activate` first, then set `PYTHONPATH` to `src` and run `uvicorn app.main:app --reload` (see the Windows run section).

### All platforms

- **`SECRET_KEY` errors** — The app requires a non-empty `SECRET_KEY` in `.env` at the project root when running Uvicorn from the repo root.
