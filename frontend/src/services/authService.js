/**
 * Auth service — handles communication with the FastAPI /auth endpoints.
 *
 * Key detail: the /auth/login endpoint follows the OAuth2 spec and expects
 * application/x-www-form-urlencoded, NOT JSON.  All other endpoints use JSON.
 */

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ─── Token storage (in-memory only — never localStorage) ────────────

let accessToken = null;
let refreshToken = null;

export const getAccessToken = () => accessToken;
export const getRefreshToken = () => refreshToken;

function parseJwtPayload(token) {
  if (!token || token.split('.').length < 2) return null;
  try {
    const payload = token.split('.')[1];
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
    return JSON.parse(atob(padded));
  } catch {
    return null;
  }
}

function isTokenExpired(token, leewaySeconds = 20) {
  const payload = parseJwtPayload(token);
  if (!payload || typeof payload.exp !== 'number') return true;
  return Date.now() >= ((payload.exp - leewaySeconds) * 1000);
}

export function setTokens(access, refresh) {
  accessToken = access;
  refreshToken = refresh;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}

// ─── Helpers ────────────────────────────────────────────────────────

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err = new Error(body.detail || `Request failed (${res.status})`);
    err.status = res.status;
    throw err;
  }

  if (res.status === 204) return null;
  return res.json();
}

/**
 * Fetch wrapper for authenticated requests.  Automatically attaches the
 * access token and retries once after refreshing if a 401 is returned.
 */
export async function authFetch(path, options = {}) {
  const withAuth = (token) => ({
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });

  try {
    return await apiFetch(path, withAuth(accessToken));
  } catch (err) {
    if (err.status !== 401 || !refreshToken) throw err;

    // Attempt a single token refresh
    try {
      await refresh();
    } catch {
      clearTokens();
      throw err;
    }

    // Retry the original request with the new token
    return apiFetch(path, withAuth(accessToken));
  }
}

// ─── Public API ─────────────────────────────────────────────────────

/**
 * Register a new account.
 * @returns {Promise<{username, email, full_name, disabled}>}
 */
export async function register(username, email, password, fullName) {
  return apiFetch('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      password,
      email: email || undefined,
      full_name: fullName || undefined,
    }),
  });
}

/**
 * Log in — sends form-urlencoded as required by the OAuth2 backend.
 * @returns {Promise<{access_token, refresh_token, token_type}>}
 */
export async function login(identifier, password) {
  const params = new URLSearchParams();
  params.append('username', identifier);
  params.append('password', password);

  const data = await apiFetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString(),
  });

  setTokens(data.access_token, data.refresh_token);
  return data;
}

/**
 * Refresh the token pair.  Old refresh token is revoked server-side.
 */
export async function refresh() {
  const data = await apiFetch('/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  setTokens(data.access_token, data.refresh_token);
  return data;
}

/**
 * Return an access token guaranteed to be present and not near expiry.
 * Refreshes once if a refresh token is available.
 */
export async function getValidAccessToken() {
  if (!accessToken) {
    if (!refreshToken) return null;
    await refresh();
    return accessToken;
  }

  if (isTokenExpired(accessToken)) {
    if (!refreshToken) return null;
    await refresh();
  }

  return accessToken;
}

/**
 * Log out — revokes both tokens server-side, clears local tokens.
 */
export async function logout() {
  try {
    await authFetch('/auth/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  } finally {
    clearTokens();
  }
}

/**
 * Reset a user's password given their username or email.
 */
export async function resetPassword(identifier, newPassword) {
  return apiFetch('/auth/reset-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier, new_password: newPassword }),
  });
}

/**
 * Fetch the current user's profile.
 */
export async function getMe() {
  return authFetch('/auth/me');
}
