import React from 'react';
import './GameList.css';

/**
 * GameList component (UC-01).
 *
 * Props:
 *   games             – array of { id, name, description, playerCount }
 *   selectedGameId    – currently selected game id (or null)
 *   onSelectGame(id)  – called when a game card is clicked
 *   onJoinLobby(id)   – called when "Join Lobby" is clicked for a game
 *   onBack()          – return to previous view
 */
function GameList({ games = [], selectedGameId, onSelectGame, onJoinLobby, onBack }) {
  const selectedGame = games.find((g) => g.id === selectedGameId);

  return (
    <div className="game-list">
      <div className="game-list-header">
        <h2 className="game-list-title">Browse Games</h2>
        {onBack && (
          <button className="game-list-back" onClick={onBack}>
            Back
          </button>
        )}
      </div>

      {games.length === 0 ? (
        <p className="game-list-empty">No games available at this time.</p>
      ) : (
        <div className="game-list-grid">
          {games.map((game) => (
            <div
              key={game.id}
              className={`game-card ${selectedGameId === game.id ? 'game-card--selected' : ''}`}
              onClick={() => onSelectGame && onSelectGame(game.id)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && onSelectGame && onSelectGame(game.id)}
            >
              <h3 className="game-card-name">{game.name}</h3>
              <p className="game-card-description">{game.description}</p>
              <span className="game-card-players">{game.playerCount} players online</span>
            </div>
          ))}
        </div>
      )}

      {selectedGame && (
        <div className="game-detail-panel">
          <h3>{selectedGame.name}</h3>
          <p>{selectedGame.description}</p>
          <p className="game-detail-players">{selectedGame.playerCount} players online</p>
          {onJoinLobby && (
            <button className="game-detail-join" onClick={() => onJoinLobby(selectedGame.id)}>
              Join Lobby
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default GameList;
