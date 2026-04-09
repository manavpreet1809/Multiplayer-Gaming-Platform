import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { getLeaderboard } from "../../services/gameService";
import Leaderboard from "./Leaderboard";

const GAME_TYPES = ["Overall", "Chess", "Tic-Tac-Toe"];

function LeaderboardPage() {
  const { user } = useContext(AuthContext);
  const [selectedGameType, setSelectedGameType] = useState(GAME_TYPES[0]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const queryType = selectedGameType.toLowerCase().replace(/[^a-z]/g, "");
        const data = await getLeaderboard(queryType);
        if (mounted) {
          setRankings(data);
        }
      } catch (err) {
        if (mounted) {
          setError(err.message || "Failed to load leaderboard.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    fetchData();
    return () => {
      mounted = false;
    };
  }, [selectedGameType]);

  return (
    <div className="leaderboard-page">
      {error && <div className="leaderboard-error">{error}</div>}
      {loading && <div className="leaderboard-loading">Loading leaderboard…</div>}
      <Leaderboard
        gameTypes={GAME_TYPES}
        selectedGameType={selectedGameType}
        onSelectGameType={setSelectedGameType}
        rankings={rankings}
        currentUsername={user?.username}
      />
    </div>
  );
}

export default LeaderboardPage;
