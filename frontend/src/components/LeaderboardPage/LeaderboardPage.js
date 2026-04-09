import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { getLeaderboard } from "../../services/gameService";
import Leaderboard from "../Leaderboard/Leaderboard";

const GAME_TYPES = ["chess", "tictactoe"];
const LABELS = { chess: "Chess", tictactoe: "TicTacToe" };

function LeaderboardPage() {
  const { user } = useContext(AuthContext);
  const [selectedGameType, setSelectedGameType] = useState(GAME_TYPES[0]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    getLeaderboard(selectedGameType)
      .then((data) => { if (!cancelled) setRankings(data); })
      .catch(() => { if (!cancelled) setError("Failed to load leaderboard."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [selectedGameType]);

  return (
    <>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      {loading && <p style={{ textAlign: "center" }}>Loading…</p>}
      <Leaderboard
        gameTypes={GAME_TYPES.map((t) => LABELS[t])}
        selectedGameType={LABELS[selectedGameType]}
        onSelectGameType={(label) => {
          const key = Object.keys(LABELS).find((k) => LABELS[k] === label);
          if (key) setSelectedGameType(key);
        }}
        rankings={rankings}
        currentUsername={user?.username}
      />
    </>
  );
}

export default LeaderboardPage;
