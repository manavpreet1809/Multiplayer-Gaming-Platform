/**
 * Game service — handles all communication with the /games endpoints.
 */

import { authFetch, getValidAccessToken } from './authService';

const WS_BASE = (process.env.REACT_APP_API_URL || 'http://localhost:8000')
  .replace(/^http/, 'ws');

// ─── REST ────────────────────────────────────────────────────────────

export function createGame(gameType, visibility = 'public') {
  return authFetch('/games/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_type: gameType, visibility }),
  });
}

export function listGames(gameType = null) {
  const q = gameType ? `?game_type=${encodeURIComponent(gameType)}` : '';
  return authFetch(`/games${q}`);
}

export function getGame(gameId) {
  return authFetch(`/games/${gameId}`);
}

export function joinGameById(gameId) {
  return authFetch(`/games/${gameId}/join`, { method: 'POST' });
}

export function joinGameByCode(lobbyCode) {
  return authFetch('/games/join/code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lobby_code: lobbyCode }),
  });
}

export function matchmake(gameType) {
  return authFetch('/games/matchmake', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_type: gameType }),
  });
}

export function startGame(gameId) {
  return authFetch(`/games/${gameId}/start`, { method: 'POST' });
}

export function leaveGame(gameId) {
  return authFetch(`/games/${gameId}/leave`, { method: 'POST' });
}

export function getLeaderboard(gameType = 'overall') {
  return authFetch(`/games/leaderboard?game_type=${encodeURIComponent(gameType)}`);
}

// ─── WebSocket helpers ────────────────────────────────────────────────

/**
 * Open a WebSocket connection to a game room.
 * Returns the raw WebSocket — caller is responsible for closing it.
 *
 * @param {string}   gameId
 * @param {function} onMessage   – called with parsed JSON data
 * @param {function} [onOpen]    – called when connection opens
 * @param {function} [onClose]   – called when connection closes
 * @param {function} [onError]   – called on error
 */
export async function createGameWebSocket(gameId, onMessage, onOpen, onClose, onError) {
  const token = await getValidAccessToken();
  if (!token) {
    throw new Error('Not authenticated. Please log in again.');
  }
  const ws = new WebSocket(`${WS_BASE}/games/ws/${gameId}?token=${encodeURIComponent(token)}`);
  ws.onopen = () => onOpen && onOpen();
  ws.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch { /* ignore malformed frames */ }
  };
  ws.onclose = (e) => onClose && onClose(e);
  ws.onerror = (e) => onError && onError(e);
  return ws;
}

/**
 * Send a move over an open game WebSocket.
 * @param {WebSocket} ws
 * @param {object}    movepayload  – chess: {from,to,promotion?}  ttt: {index}
 */
export function sendMove(ws, movePayload) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'move', move: movePayload }));
  }
}

/**
 * Request legal moves for the piece at (row, col) over the game WebSocket.
 * Server responds with a "legal_moves" message.
 */
export function sendSelectPiece(ws, row, col) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'select_piece', position: { row, col } }));
  }
}

/**
 * Send a lobby/game chat message over the game WebSocket.
 */
export function sendGameChat(ws, text) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'chat', text }));
  }
}

/**
 * Open a WebSocket connection to the global chat room.
 */
export async function createGlobalChatWebSocket(onMessage, onOpen, onClose, onError) {
  const token = await getValidAccessToken();
  if (!token) {
    throw new Error('Not authenticated. Please log in again.');
  }
  const ws = new WebSocket(`${WS_BASE}/games/chat/global?token=${encodeURIComponent(token)}`);
  ws.onopen = () => onOpen && onOpen();
  ws.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch { /* ignore */ }
  };
  ws.onclose = (e) => onClose && onClose(e);
  ws.onerror = (e) => onError && onError(e);
  return ws;
}

/**
 * Send a message on the global chat WebSocket.
 */
export function sendGlobalChat(ws, text) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'chat', text }));
  }
}
