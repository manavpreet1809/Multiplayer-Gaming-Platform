import React from 'react';
import './Leaderboard.css';

/**
 * Leaderboard component (UC-12).
 *
 * Props:
 *   gameTypes              – array of game type strings (e.g. ["Connect 4", "Tic-Tac-Toe", "Checkers", "Overall"])
 *   selectedGameType       – currently selected game type
 *   onSelectGameType(type) – switch the displayed leaderboard
 *   rankings               – array of { rank, username, tier, mmr, wins, losses }
 *   currentUsername         – logged-in player's username (to highlight their row)
 *   onBack()               – return to dashboard
 */
function Leaderboard({
  gameTypes = [],
  selectedGameType,
  onSelectGameType,
  rankings = [],
  currentUsername,
  onBack,
}) {
  return (
    <div className="leaderboard">
      <div className="leaderboard-header">
        <h2 className="leaderboard-title">Leaderboard</h2>
        {onBack && (
          <button className="leaderboard-back" onClick={onBack}>
            Back to Dashboard
          </button>
        )}
      </div>

      {gameTypes.length > 0 && (
        <div className="leaderboard-tabs">
          {gameTypes.map((type) => (
            <button
              key={type}
              className={`leaderboard-tab ${selectedGameType === type ? 'leaderboard-tab--active' : ''}`}
              onClick={() => onSelectGameType && onSelectGameType(type)}
            >
              {type}
            </button>
          ))}
        </div>
      )}

      {rankings.length === 0 ? (
        <p className="leaderboard-empty">No rankings available yet.</p>
      ) : (
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Player</th>
              <th>Rank</th>
              <th>MMR</th>
              <th>W/L</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((entry) => (
              <tr
                key={entry.rank}
                className={entry.username === currentUsername ? 'leaderboard-row--current' : ''}
              >
                <td>{entry.rank}</td>
                <td>{entry.username}</td>
                <td>{entry.tier}</td>
                <td>{entry.mmr}</td>
                <td>{entry.wins}/{entry.losses}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {currentUsername && rankings.length > 0 && !rankings.some((r) => r.username === currentUsername) && (
        <p className="leaderboard-note">Play more games to appear on the leaderboard.</p>
      )}
    </div>
  );
}

export default Leaderboard;
