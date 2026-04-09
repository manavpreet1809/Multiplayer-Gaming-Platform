import "./Leaderboard.css";
import { useNavigate } from "react-router-dom";

/**
 * Leaderboard component (UC-12).
 *
 * Props:
 *   gameTypes              – array of game type strings (e.g. ["Connect 4", "Tic-Tac-Toe", "Checkers", "Overall"])
 *   selectedGameType       – currently selected game type
 *   onSelectGameType(type) – switch the displayed leaderboard
 *   rankings               – array of { place, username, tier, mmr, wins, losses, ties?, rank? }
 *   currentUsername         – logged-in player's username (to highlight their row)
 */
function Leaderboard({
  gameTypes = [],
  selectedGameType,
  onSelectGameType,
  rankings = [],
  currentUsername,
}) {
  const navigate = useNavigate();

  return (
    <div className="leaderboard">
      <div className="leaderboard-header">
        <h2 className="leaderboard-title">Leaderboard</h2>

        <button
          className="leaderboard-back"
          onClick={() => navigate("/dashboard")}
        >
          Back to Dashboard
        </button>
      </div>

      {gameTypes.length > 0 && (
        <div className="leaderboard-tabs">
          {gameTypes.map((type) => (
            <button
              key={type}
              className={`leaderboard-tab ${selectedGameType === type ? "leaderboard-tab--active" : ""}`}
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
              <th scope="col">#</th>
              <th scope="col">Player</th>
              <th scope="col">Rank</th>
              <th scope="col">MMR</th>
              <th scope="col">W/L/T</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((entry, index) => (
              <tr
                key={`${entry.username}-${entry.place ?? index}`}
                className={
                  entry.username === currentUsername
                    ? "leaderboard-row--current"
                    : ""
                }
              >
                <td>{entry.place ?? index + 1}</td>
                <td>{entry.username}</td>
                <td>{entry.tier ?? entry.rank}</td>
                <td>{entry.mmr}</td>
                <td>
                  {entry.wins}/{entry.losses}/{entry.ties ?? 0}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {currentUsername &&
        rankings.length > 0 &&
        !rankings.some((r) => r.username === currentUsername) && (
          <p className="leaderboard-note">
            Play more games to appear on the leaderboard.
          </p>
        )}
    </div>
  );
}

export default Leaderboard;
