import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import "./Dashboard.css";

/**
 * Dashboard component (UC-04).
 *
 * Props:
 *   username          – display name of the authenticated player
 *   status            – player status: "idle" | "in-lobby" | "in-queue" | "game-ready"
 *   notifications     – array of { id, message } notification objects
 *   onBrowseGames()   – navigate to game list (UC-01)
 *   onCreateGame()    – create a new game lobby
 *   onJoinGame()      – join an existing game lobby (UC-05)
 *   onEnqueue()       – enqueue for matchmaking (UC-06)
 *   onOpenChat()      – open the chat panel (UC-07)
 *   onJoinActiveGame()– join a ready game session (UC-08)
 *   onViewProfile()   – navigate to profile (UC-09)
 *   onLeaderboard()   – navigate to leaderboard (UC-12)
 *   onLogout()        – log out (AUTH-04)
 */
function Dashboard({
  status = "idle",
  notifications = [],
  onBrowseGames,
  onCreateGame,
  onJoinGame,
  onEnqueue,
  onOpenChat,
  onJoinActiveGame,
  onViewProfile,
  onLeaderboard,
}) {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <div className="dashboard-user-info">
          <span className="dashboard-username">{user?.username}</span>
          <span className={`dashboard-status dashboard-status--${status}`}>
            {status.replace("-", " ")}
          </span>
        </div>
        <nav className="dashboard-nav">
          {onViewProfile && (
            <button className="dashboard-nav-link" onClick={onViewProfile}>
              Profile
            </button>
          )}
          {onLeaderboard && (
            <button className="dashboard-nav-link" onClick={onLeaderboard}>
              Leaderboard
            </button>
          )}

          <button
            className="dashboard-nav-link dashboard-nav-link--logout"
            onClick={handleLogout}
          >
            Log Out
          </button>
        </nav>
      </header>

      {notifications.length > 0 && (
        <section className="dashboard-notifications">
          <h3>Notifications</h3>
          <ul>
            {notifications.map((n) => (
              <li key={n.id} className="dashboard-notification">
                {n.message}
              </li>
            ))}
          </ul>
        </section>
      )}

      {status === "game-ready" && onJoinActiveGame && (
        <div className="dashboard-banner dashboard-banner--game-ready">
          <span>A game is ready for you!</span>
          <button
            className="dashboard-action dashboard-action--primary"
            onClick={onJoinActiveGame}
          >
            Join Game
          </button>
        </div>
      )}

      {status === "in-queue" && (
        <div className="dashboard-banner dashboard-banner--in-queue">
          <span>You are currently in the matchmaking queue…</span>
        </div>
      )}

      {status === "in-lobby" && (
        <div className="dashboard-banner dashboard-banner--in-lobby">
          <span>You are currently in a game lobby.</span>
        </div>
      )}

      <section className="dashboard-actions">
        <h2>What would you like to do?</h2>
        <div className="dashboard-action-grid">
          {onBrowseGames && (
            <button className="dashboard-action" onClick={onBrowseGames}>
              Browse Games
            </button>
          )}
          {onCreateGame && (
            <button className="dashboard-action" onClick={onCreateGame}>
              Create Game
            </button>
          )}
          {onJoinGame && (
            <button className="dashboard-action" onClick={onJoinGame}>
              Join Game
            </button>
          )}
          {onEnqueue && (
            <button className="dashboard-action" onClick={onEnqueue}>
              Find Match
            </button>
          )}
          {onOpenChat && (
            <button className="dashboard-action" onClick={onOpenChat}>
              Open Chat
            </button>
          )}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
