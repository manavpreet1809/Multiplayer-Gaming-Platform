import React from 'react';
import './GameLobby.css';

/**
 * GameLobby component (UC-05).
 *
 * Props:
 *   lobbyId            – unique lobby identifier
 *   gameName           – name of the game this lobby is for
 *   status             – "waiting" | "started"
 *   players            – array of { id, username, isReady }
 *   requiredPlayers    – number of players needed to start
 *   onLeaveLobby()     – leave this lobby
 *   onToggleReady()    – toggle ready status
 *   onStartGame()      – start the game (lobby leader only)
 *   chatComponent      – optional React node for embedded chat (UC-07)
 */
function GameLobby({
  lobbyId,
  gameName,
  status = 'waiting',
  players = [],
  requiredPlayers = 2,
  onLeaveLobby,
  onToggleReady,
  onStartGame,
  chatComponent,
}) {
  const canStart = status === 'waiting' && players.length >= requiredPlayers;

  return (
    <div className="game-lobby">
      <div className="game-lobby-header">
        <div>
          <h2 className="game-lobby-title">{gameName} Lobby</h2>
          <span className="game-lobby-id">Lobby ID: {lobbyId}</span>
        </div>
        <div className="game-lobby-header-actions">
          <span className={`game-lobby-status game-lobby-status--${status}`}>
            {status === 'waiting' ? 'Waiting for players' : 'Game Started'}
          </span>
          {onLeaveLobby && (
            <button className="game-lobby-leave" onClick={onLeaveLobby}>
              Leave Lobby
            </button>
          )}
        </div>
      </div>

      <section className="game-lobby-players">
        <h3>
          Players ({players.length}/{requiredPlayers})
        </h3>
        <ul className="game-lobby-player-list">
          {players.map((player) => (
            <li key={player.id} className="game-lobby-player">
              <span className="game-lobby-player-name">{player.username}</span>
              <span
                className={`game-lobby-player-status ${
                  player.isReady ? 'game-lobby-player-status--ready' : ''
                }`}
              >
                {player.isReady ? 'Ready' : 'Not Ready'}
              </span>
            </li>
          ))}
          {Array.from({ length: requiredPlayers - players.length }).map((_, i) => (
            <li key={`empty-${i}`} className="game-lobby-player game-lobby-player--empty">
              <span className="game-lobby-player-name">Waiting for player…</span>
            </li>
          ))}
        </ul>
      </section>

      <div className="game-lobby-actions">
        {onToggleReady && status === 'waiting' && (
          <button className="game-lobby-ready" onClick={onToggleReady}>
            Toggle Ready
          </button>
        )}
        {onStartGame && canStart && (
          <button className="game-lobby-start" onClick={onStartGame}>
            Start Game
          </button>
        )}
      </div>

      {chatComponent && (
        <section className="game-lobby-chat">
          {chatComponent}
        </section>
      )}
    </div>
  );
}

export default GameLobby;
