import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import "./Profile.css";
import { AuthContext } from "../../context/AuthContext";

/**
 * Profile component (UC-09).
 *
 * Props:
 *   username, email  – optional display fallbacks when AuthContext.user is absent (e.g. screenshot page)
 *   generalStats    – { gamesPlayed, wins, losses, ties }
 *   gameStats       – array of { gameType, gamesPlayed, wins, losses, rank, mmr }
 *   onEditSettings()– navigate to account settings (UC-10)
 */
function Profile({
  generalStats,
  gameStats,
  onEditSettings,
  username: usernameProp,
  email: emailProp,
}) {
  const ctx = useContext(AuthContext);
  const user = ctx?.user;
  const navigate = useNavigate();
  const displayUsername = user?.username ?? usernameProp ?? "";
  const displayEmail = user?.email ?? emailProp ?? "";

  const inheritedGeneral = user?.stats?.overall || {};
  const general = {
    gamesPlayed:
      generalStats?.gamesPlayed ?? generalStats?.games_played ?? inheritedGeneral?.games_played ?? 0,
    wins: generalStats?.wins ?? inheritedGeneral?.wins ?? 0,
    losses: generalStats?.losses ?? inheritedGeneral?.losses ?? 0,
    ties: generalStats?.ties ?? inheritedGeneral?.ties ?? 0,
  };

  const gameStatsFromUser = user?.stats?.games
    ? Object.entries(user.stats.games)
        .map(([gameType, stats]) => ({
          gameType:
            gameType === "tictactoe"
              ? "Tic-Tac-Toe"
              : gameType.charAt(0).toUpperCase() + gameType.slice(1),
          gamesPlayed: stats.games_played ?? stats.gamesPlayed ?? 0,
          wins: stats.wins ?? 0,
          losses: stats.losses ?? 0,
          ties: stats.ties ?? 0,
          rank: stats.rank || "Bronze",
          mmr: stats.mmr ?? 0,
        }))
        .filter((row) => row.gamesPlayed > 0)
    : [];

  const displayGameStats = gameStats?.length > 0 ? gameStats : gameStatsFromUser;
  const hasPlayed = general.gamesPlayed > 0;

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
          <span className="profile-field-value">{displayUsername}</span>
        </div>
        <div className="profile-field">
          <span className="profile-field-label">Email</span>
          <span className="profile-field-value">{displayEmail}</span>
        </div>
      </section>

      <section className="profile-stats">
        <h3>Overall Stats</h3>
        {hasPlayed ? (
          <div className="profile-stat-grid">
            <div className="profile-stat">
              <span className="profile-stat-value">
                {general.gamesPlayed}
              </span>
              <span className="profile-stat-label">Games Played</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{general.wins}</span>
              <span className="profile-stat-label">Wins</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{general.losses}</span>
              <span className="profile-stat-label">Losses</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{general.ties}</span>
              <span className="profile-stat-label">Ties</span>
            </div>
          </div>
        ) : (
          <p className="profile-no-data">No games played yet.</p>
        )}
      </section>

      {displayGameStats.length > 0 && (
        <section className="profile-game-stats">
          <h3>Per-Game Stats</h3>
          <table className="profile-table">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Played</th>
                <th scope="col">W</th>
                <th scope="col">L</th>
                <th scope="col">T</th>
                <th scope="col">Rank</th>
                <th scope="col">MMR</th>
              </tr>
            </thead>
            <tbody>
              {displayGameStats.map((gs) => (
                <tr key={gs.gameType}>
                  <td>{gs.gameType}</td>
                  <td>{gs.gamesPlayed}</td>
                  <td>{gs.wins}</td>
                  <td>{gs.losses}</td>
                  <td>{gs.ties ?? 0}</td>
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
