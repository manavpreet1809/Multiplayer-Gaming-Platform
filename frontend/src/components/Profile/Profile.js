import React from 'react';
import './Profile.css';

/**
 * Profile component (UC-09).
 *
 * Props:
 *   username        – player's username
 *   email           – player's email
 *   generalStats    – { gamesPlayed, wins, losses, ties }
 *   gameStats       – array of { gameType, gamesPlayed, wins, losses, rank, mmr }
 *   onEditSettings()– navigate to account settings (UC-10)
 *   onBack()        – return to dashboard
 */
function Profile({
  username,
  email,
  generalStats = { gamesPlayed: 0, wins: 0, losses: 0, ties: 0 },
  gameStats = [],
  onEditSettings,
  onBack,
}) {
  const hasPlayed = generalStats.gamesPlayed > 0;

  return (
    <div className="profile">
      <div className="profile-header">
        <h2 className="profile-title">Player Profile</h2>
        {onBack && (
          <button className="profile-back" onClick={onBack}>
            Back to Dashboard
          </button>
        )}
      </div>

      <section className="profile-info">
        <div className="profile-field">
          <span className="profile-field-label">Username</span>
          <span className="profile-field-value">{username}</span>
        </div>
        <div className="profile-field">
          <span className="profile-field-label">Email</span>
          <span className="profile-field-value">{email}</span>
        </div>
      </section>

      <section className="profile-stats">
        <h3>Overall Stats</h3>
        {hasPlayed ? (
          <div className="profile-stat-grid">
            <div className="profile-stat">
              <span className="profile-stat-value">{generalStats.gamesPlayed}</span>
              <span className="profile-stat-label">Games Played</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{generalStats.wins}</span>
              <span className="profile-stat-label">Wins</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{generalStats.losses}</span>
              <span className="profile-stat-label">Losses</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{generalStats.ties}</span>
              <span className="profile-stat-label">Ties</span>
            </div>
          </div>
        ) : (
          <p className="profile-no-data">No games played yet.</p>
        )}
      </section>

      {gameStats.length > 0 && (
        <section className="profile-game-stats">
          <h3>Per-Game Stats</h3>
          <table className="profile-table">
            <thead>
              <tr>
                <th>Game</th>
                <th>Played</th>
                <th>W</th>
                <th>L</th>
                <th>Rank</th>
                <th>MMR</th>
              </tr>
            </thead>
            <tbody>
              {gameStats.map((gs) => (
                <tr key={gs.gameType}>
                  <td>{gs.gameType}</td>
                  <td>{gs.gamesPlayed}</td>
                  <td>{gs.wins}</td>
                  <td>{gs.losses}</td>
                  <td>{gs.rank}</td>
                  <td>{gs.mmr}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {onEditSettings && (
        <div className="profile-actions">
          <button className="profile-edit" onClick={onEditSettings}>
            Edit Account Settings
          </button>
        </div>
      )}
    </div>
  );
}

export default Profile;
