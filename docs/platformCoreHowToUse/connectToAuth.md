# Auth Service

A FastAPI authentication backend with MongoDB. Provides JWT-based registration, login, logout, and token refresh endpoints for use with a React/TypeScript frontend.

---

## How It Works

This service handles everything related to user identity: creating accounts, proving who you are, and revoking access when you log out. Here's what each piece does:

### User Registration
When a user registers, their password is validated against a set of rules (8+ characters, uppercase, lowercase, digit, special character) before anything hits the database. The password is then hashed using Argon2 (via `pwdlib`) and stored the plaintext password is never saved anywhere. A unique index on both `username` and `email` in MongoDB enforces that no two users can share either.

### Login & JWT Tokens
Login accepts a username and password. If valid, the service issues two tokens:
- **Access token**:  short-lived (30 minutes). Sent with every API request in the `Authorization` header. Contains the username, a token type, and a unique ID (`jti`).
- **Refresh token**:  long-lived (7 days). Used only to get a new access token when the old one expires.

Both tokens are signed with `SECRET_KEY` using HS256. This means the server can verify a token is genuine without hitting the database on every request.

### Token Blocklist
Every token has a unique `jti` (JWT ID). When a user logs out or refreshes, the old token's `jti` is written to a `revoked_tokens` collection in MongoDB. On every protected request, the service does a single indexed lookup to check if the token has been revoked. MongoDB's TTL index automatically deletes blocklist entries once the token would have expired anyway, keeping the collection small.

### Refresh Token Rotation
When a refresh token is used to get a new token pair, the old refresh token is immediately revoked. This means each refresh token can only be used once if an attacker steals one and tries to use it after the legitimate user already has, it will be rejected.

### Logout
Logout revokes both the access token and the refresh token simultaneously, immediately invalidating the session on the server side.

### Security Details
- **Timing-safe authentication**: if a username doesn't exist, the service still runs a password hash comparison against a dummy hash. This prevents attackers from figuring out which usernames exist based on response time.
- **Rate limiting**: login is capped at 10 requests/minute per IP, refresh at 20/minute. Exceeding this returns a `429 Too Many Requests`.
- **SECRET_KEY enforcement**:the app refuses to start if `SECRET_KEY` is missing or left as the default value.

---

## Backend Setup

### Prerequisites

- Python 3.10+
- MongoDB running locally or a connection string to a hosted instance

### Install dependencies

```bash
/opt/homebrew/bin/python3.10 -m pip install \
  fastapi \
  uvicorn \
  "pymongo[srv]" \
  pyjwt \
  "pwdlib[argon2]" \
  slowapi \
  "pydantic[email]" \
  python-multipart \
  python-dotenv
```

### Environment variables

Create a `.env` file at `src/app/.env`:

```bash
# Generate with: python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=

# MongoDB
MONGODB_URL=mongodb://localhost:27017
DB_NAME=myapp

# Token expiry
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> **Important:** `SECRET_KEY` must be set before the app will start. Never commit `.env` to version control.

### Run the server

```bash
uvicorn src.app.main:app --reload
```

API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

---

## API Reference

### `POST /auth/register`
Create a new user account.

**Request body (JSON):**
```json
{
  "username": "geff",
  "password": "MyPassword1!",
  "email": "geff@example.com",
  "full_name": "Geff Smith"
}
```

Password must contain: 8+ characters, uppercase, lowercase, digit, special character.

**Response `201`:**
```json
{
  "username": "geff",
  "email": "geff@example.com",
  "full_name": "Geff Smith",
  "disabled": false
}
```

---

### `POST /auth/login`
Log in and receive an access + refresh token pair.

**Request body (`application/x-www-form-urlencoded`):**
```
username=geff&password=MyPassword1!
```

> Note: Login uses form encoding, not JSON. This is required by the OAuth2 standard.

**Response `200`:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```

Rate limited to **10 requests/minute** per IP.

---

### `POST /auth/refresh`
Exchange a valid refresh token for a new access + refresh token pair. The old refresh token is invalidated immediately.

**Request body (JSON):**
```json
{
  "refresh_token": "<jwt>"
}
```

**Response `200`:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```

---

### `POST /auth/logout`
Revoke both the current access token and the refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request body (JSON):**
```json
{
  "refresh_token": "<jwt>"
}
```

**Response `204` (no content)**

---

### `GET /auth/me`
Returns the currently authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response `200`:**
```json
{
  "username": "geff",
  "email": "geff@example.com",
  "full_name": "Geff Smith",
  "disabled": false
}
```

---

## Testing Guide

The interactive Swagger UI at `http://localhost:8000/docs` lets you test all endpoints directly in the browser without any extra tooling. For scripted or automated testing, use the scenarios below.

---

### Registration(Testing Team):  what to test

**Happy path**
- Register with a valid username, password, email, and full name → expect `201` and the user object back (no password field in the response)
- Register with only username and password (email and full_name are optional) → expect `201`

**Password validation: each of these should return `400`**
- Password under 8 characters: `"abc1!A"`
- No uppercase letter: `"mypassword1!"`
- No lowercase letter: `"MYPASSWORD1!"`
- No digit: `"MyPassword!"`
- No special character: `"MyPassword1"`

**Duplicate users: should return `400`**
- Register the same username twice → expect `400` with `"Username already exists"`
- Register with the same email twice → expect `400` with `"Email already in use"`

---

### Login(Testing Team): what to test

> Remember: login sends `application/x-www-form-urlencoded`, not JSON.

**Happy path**
- Valid username and password → expect `200` with both `access_token` and `refresh_token`

**Failure cases**
- Wrong password → expect `401`
- Non-existent username → expect `401` (same error message as wrong password this is intentional, it prevents username enumeration)
- Sending JSON instead of form data → expect `422`

**Rate limiting**
- Send 11+ login requests in under a minute from the same IP → expect `429` on the 11th request

---

### Protected routes (`/auth/me`): what to test

- Valid access token in `Authorization: Bearer <token>` header → expect `200` with user profile
- No token → expect `401`
- Malformed token (e.g. `"Bearer garbage"`) → expect `401`
- Expired token → expect `401` (set `ACCESS_TOKEN_EXPIRE_MINUTES=0` in `.env` to test this quickly)
- Using a refresh token where an access token is expected → expect `401` (tokens carry a `type` claim that is validated)

---

### Refresh(Testing Team): what to test

**Happy path**
- Send a valid refresh token → expect `200` with a new token pair
- Verify the old refresh token is now invalid by trying to use it again → expect `401`

**Failure cases**
- Send an access token to `/auth/refresh` instead of a refresh token → expect `401`
- Send an expired refresh token → expect `401`
- Send a garbage string → expect `401`

---

### Logout(Testing Team): what to test

**Happy path**
- Log in, then call `/auth/logout` with the access token in the header and refresh token in the body → expect `204`
- After logout, try to use the access token on `/auth/me` → expect `401`
- After logout, try to use the refresh token on `/auth/refresh` → expect `401`

**Failure cases**
- Call `/auth/logout` without an access token → expect `401`
- Call `/auth/logout` with a valid access token but missing `refresh_token` in the body → expect `422`

---

### Things to be aware of

- **MongoDB must be running** before starting the server: if it isn't, the app will start but all requests will fail with 500 errors
- **`.env` must have `SECRET_KEY` set**: the app will refuse to start without it
- **Token expiry times are configurable** via `.env`: set `ACCESS_TOKEN_EXPIRE_MINUTES` to a low number like `1` to test expiry scenarios without waiting
- **The blocklist is in MongoDB**: if you wipe the `revoked_tokens` collection manually, previously revoked tokens will become valid again until they naturally expire

---

## Connecting from React/TypeScript

### Install frontend dependencies

```bash
npm install axios
```

### Token storage

Store both tokens in memory (a React context or Zustand store). Do **not** store them in `localStorage` it is accessible to JavaScript and vulnerable to XSS attacks.

```ts
// src/auth/tokenStore.ts
let accessToken: string | null = null;
let refreshToken: string | null = null;

export const setTokens = (access: string, refresh: string) => {
  accessToken = access;
  refreshToken = refresh;
};

export const getAccessToken = () => accessToken;
export const getRefreshToken = () => refreshToken;

export const clearTokens = () => {
  accessToken = null;
  refreshToken = null;
};
```

---

### Register

```ts
// src/auth/api.ts
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const register = async (
  username: string,
  password: string,
  email?: string,
  fullName?: string
) => {
  const { data } = await axios.post(`${BASE_URL}/auth/register`, {
    username,
    password,
    email,
    full_name: fullName,
  });
  return data;
};
```

---

### Login

Note: login requires `application/x-www-form-urlencoded`, not JSON. Use `URLSearchParams` for this.

```ts
import { setTokens } from './tokenStore';

export const login = async (username: string, password: string) => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const { data } = await axios.post(`${BASE_URL}/auth/login`, params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  setTokens(data.access_token, data.refresh_token);
  return data;
};
```

---

### Making authenticated requests

Always attach the access token in the `Authorization` header:

```ts
import { getAccessToken } from './tokenStore';

export const getMe = async () => {
  const { data } = await axios.get(`${BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });
  return data;
};
```

---

### Refresh token handling

When a request fails with `401`, automatically try to refresh and retry. The easiest way is an Axios response interceptor:

```ts
import axios from 'axios';
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './tokenStore';

const api = axios.create({ baseURL: BASE_URL });

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// On 401, try to refresh once then retry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const { data } = await axios.post(`${BASE_URL}/auth/refresh`, {
          refresh_token: getRefreshToken(),
        });
        setTokens(data.access_token, data.refresh_token);
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return api(original);
      } catch {
        // Refresh failed: session is over
        clearTokens();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

Use `api` instead of `axios` directly for all authenticated requests and token refresh will be handled automatically.

---

### Logout

```ts
import { getRefreshToken, clearTokens } from './tokenStore';

export const logout = async () => {
  try {
    await api.post('/auth/logout', {
      refresh_token: getRefreshToken(),
    });
  } finally {
    // Always clear local tokens even if the request fails
    clearTokens();
    window.location.href = '/login';
  }
};
```

---

## Project Structure

```
src/app/
├── api/
│   └── auth.py              # Route handlers (register, login, refresh, logout, me)
├── db/
│   └── validUser_mongo.py   # MongoDB client + index setup
├── schemas/
│   └── auth.py              # Pydantic models + password validation
├── services/
│   └── authServices.py      # Business logic, JWT creation, blocklist, user helpers
├── .env                     # Environment variables (never commit)
├── __init__.py
└── main.py                  # App entry point, lifespan, rate limiter setup
```