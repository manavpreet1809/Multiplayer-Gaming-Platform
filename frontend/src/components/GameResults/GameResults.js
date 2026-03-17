import React from 'react';
import './GameResults.css';

/**
 * GameResults component (UC-14).
 *
 * Props:
 *   result             – "win" | "loss" | "draw"
 *   winnerUsername      – username of the winner (or null for draw)
 *   mmrChange          – number (positive or negative)
 *   newRank            – updated rank string (or null if unchanged)
 *   onReturnDashboard()– go back to dashboard
 *   onPlayAgain()      – re-enqueue for same game type (UC-06)
 *   onViewLeaderboard()– navigate to leaderboard (UC-12)
 */
function GameResults({
  result,
  winnerUsername,
  mmrChange,
  newRank,
  onReturnDashboard,
  onPlayAgain,
  onViewLeaderboard,
}) {
  const resultLabel = result === 'draw' ? 'Draw' : result === 'win' ? 'Victory!' : 'Defeat';
  const resultClass = result === 'draw' ? 'draw' : result === 'win' ? 'win' : 'loss';

  return (
    <div className="game-results">
      <div className={`game-results-banner game-results-banner--${resultClass}`}>
        <h2 className="game-results-label">{resultLabel}</h2>
        {winnerUsername && result !== 'draw' && (
          <p className="game-results-winner">Winner: {winnerUsername}</p>
        )}
      </div>

      <section className="game-results-stats">
        {mmrChange !== undefined && mmrChange !== null && (
          <div className="game-results-stat">
            <span className="game-results-stat-label">MMR Change</span>
            <span
              className={`game-results-stat-value ${
                mmrChange >= 0 ? 'game-results-stat-value--positive' : 'game-results-stat-value--negative'
              }`}
            >
              {mmrChange >= 0 ? `+${mmrChange}` : mmrChange}
            </span>
          </div>
        )}
        {newRank && (
          <div className="game-results-stat">
            <span className="game-results-stat-label">New Rank</span>
            <span className="game-results-stat-value">{newRank}</span>
          </div>
        )}
      </section>

      <div className="game-results-actions">
        {onReturnDashboard && (
          <button className="game-results-action" onClick={onReturnDashboard}>
            Return to Dashboard
          </button>
        )}
        {onPlayAgain && (
          <button className="game-results-action game-results-action--primary" onClick={onPlayAgain}>
            Play Again
          </button>
        )}
        {onViewLeaderboard && (
          <button className="game-results-action" onClick={onViewLeaderboard}>
            View Leaderboard
          </button>
        )}
      </div>
    </div>
  );
}

export default GameResults;
