/**
 * Adapter utilities that convert serialized backend game state
 * into the prop formats expected by ChessBoard and TicTacToeBoard components.
 *
 * These handle the data-shape mismatches between the rules-validation
 * team's Python engine output and the client-UI React components.
 */

// ─── Chess ───────────────────────────────────────────────────────────

/**
 * Convert serialized chess engine state into ChessBoard component props.
 *
 * The backend's serializeState() already handles:
 *   - Row-flip (backend row 0 = white back rank → frontend row 0 = rank 8)
 *   - Piece codes (uppercase = white, lowercase = black)
 *
 * This adapter maps the remaining fields into the prop names the component expects.
 *
 * @param {object}  state        – serialized state from ChessEngine.serializeState()
 * @param {string}  localPlayer  – "white" or "black" (who is sitting at this client)
 * @param {object}  [extra]      – optional overrides (selectedSquare, highlightedSquares, etc.)
 * @returns {object} props ready to spread onto <ChessBoard {...props} />
 */
export function chessStateToProps(state, localPlayer, extra = {}) {
  const opponentColor = localPlayer === 'white' ? 'black' : 'white';
  const players = state?.players || {};

  return {
    board: state?.board || [],                   // 8x8 array of piece codes / null
    currentPlayer: state?.activeColor || 'white',// "white" | "black"
    isMyTurn: state?.activeColor === localPlayer,
    playerColor: localPlayer,
    opponentName: players[opponentColor] || opponentColor,
    // These are typically managed by frontend interaction state:
    selectedSquare: extra.selectedSquare ?? null,
    highlightedSquares: extra.highlightedSquares ?? [],
    lastMove: extra.lastMove ?? null,
    capturedByWhite: extra.capturedByWhite ?? [],
    capturedByBlack: extra.capturedByBlack ?? [],
  };
}

/**
 * Build the move payload the backend expects from a UI interaction.
 *
 * @param {{row: number, col: number}} from – source square (frontend coords)
 * @param {{row: number, col: number}} to   – target square (frontend coords)
 * @param {string} [promotion]              – piece code for pawn promotion ("Q","R","B","N")
 * @returns {object} move dict for ChessEngine.deserializeMove()
 */
export function buildChessMove(from, to, promotion = null) {
  const move = { from, to };
  if (promotion) move.promotion = promotion;
  return move;
}

// ─── Tic-Tac-Toe ────────────────────────────────────────────────────

/**
 * Convert serialized TTT engine state into TicTacToeBoard component props.
 *
 * The backend's serializeState() already handles:
 *   - 2D grid → flat 9-element array
 *   - Player names → "X"/"O" symbols
 *
 * @param {object}  state        – serialized state from TicTacToeEngine.serializeState()
 * @param {string}  localSymbol  – "X" or "O" (this client's symbol)
 * @param {object}  [extra]      – optional overrides (winningCells, etc.)
 * @returns {object} props ready to spread onto <TicTacToeBoard {...props} />
 */
export function tttStateToProps(state, localSymbol, extra = {}) {
  const opponentSymbol = localSymbol === 'X' ? 'O' : 'X';
  const players = state?.players || {};

  return {
    board: state?.board || Array(9).fill(null),    // flat array of 9: "X" | "O" | null
    currentPlayer: state?.currentPlayer || 'X',    // "X" | "O"
    isMyTurn: state?.currentPlayer === localSymbol,
    playerSymbol: localSymbol,
    opponentName: players[opponentSymbol] || opponentSymbol,
    winningCells: extra.winningCells ?? null,
  };
}

/**
 * Build the move payload the backend expects from a cell click.
 *
 * @param {number} index – cell index 0-8
 * @returns {object} move dict for TicTacToeEngine.deserializeMove()
 */
export function buildTttMove(index) {
  return { index };
}

// ─── Game Results ────────────────────────────────────────────────────

/**
 * Convert the backend's serializeEndResult() output into GameResults component props.
 *
 * @param {object} endResult      – serialized end result (e.g. {isOver, result, winner, reason})
 *                                  winner is already a string: "white"/"black" (chess) or "X"/"O" (ttt)
 * @param {string} localPlayer    – the local player identifier ("white"/"black" or "X"/"O")
 * @param {object} [playerNames]  – optional map of identifiers to display names,
 *                                  e.g. {white: "Alice", black: "Bob"} or {X: "Alice", O: "Bob"}
 * @param {object} [rankInfo]     – optional {mmrChange, newRank} from the server
 * @returns {object} props for <GameResults />, or null if game is not over
 */
export function endResultToProps(endResult, localPlayer, playerNames = {}, rankInfo = {}) {
  if (!endResult || !endResult.isOver) return null;

  let result;
  if (endResult.result === 'draw') {
    result = 'draw';
  } else if (endResult.winner === localPlayer) {
    result = 'win';
  } else {
    result = 'loss';
  }

  // Resolve winner identifier to a display username if mapping is available
  const winnerKey = endResult.winner ?? null;
  const winnerUsername = (winnerKey && playerNames[winnerKey]) || winnerKey;

  return {
    result,
    winnerUsername,
    mmrChange: rankInfo.mmrChange ?? null,
    newRank: rankInfo.newRank ?? null,
  };
}
