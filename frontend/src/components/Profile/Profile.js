import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import "./Profile.css";
import { AuthContext } from "../../context/AuthContext";

/**
 * Profile component (UC-09).
 *
 * Props:
 *   generalStats    – { gamesPlayed, wins, losses, ties }
 *   gameStats       – array of { gameType, gamesPlayed, wins, losses, rank, mmr }
 *   onEditSettings()– navigate to account settings (UC-10)
 */
function Profile({
  generalStats = { gamesPlayed: 0, wins: 0, losses: 0, ties: 0 },
  gameStats = [],
  onEditSettings,
}) {
  const hasPlayed = generalStats.gamesPlayed > 0;
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div className="profile">
      <div className="profile-header">
        <h2 className="profile-title">Player Profile</h2>

        <button className="profile-back" onClick={() => navigate("/dashboard")}>
          Back to Dashboard
        </button>
      </div>

      <section className="profile-info">
        <div className="profile-field">
          <span className="profile-field-label">Username</span>
          <span className="profile-field-value">{user.username}</span>
        </div>
        <div className="profile-field">
          <span className="profile-field-label">Email</span>
          <span className="profile-field-value">{user.email}</span>
        </div>
      </section>

      <section className="profile-stats">
        <h3>Overall Stats</h3>
        {hasPlayed ? (
          <div className="profile-stat-grid">
            <div className="profile-stat">
              <span className="profile-stat-value">
                {generalStats.gamesPlayed}
              </span>
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
                <th scope="col">Game</th>
                <th scope="col">Played</th>
                <th scope="col">W</th>
                <th scope="col">L</th>
                <th scope="col">Rank</th>
                <th scope="col">MMR</th>
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
