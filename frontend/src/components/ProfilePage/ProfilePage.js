import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { getUserStats } from "../../services/gameService";
import Profile from "../Profile/Profile";

function ProfilePage() {
  const { user } = useContext(AuthContext);
  const [generalStats, setGeneralStats] = useState({
    gamesPlayed: 0,
    wins: 0,
    losses: 0,
    ties: 0,
  });
  const [gameStats, setGameStats] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user?.username) return;
    getUserStats(user.username)
      .then((data) => {
        setGeneralStats(data.generalStats);
        setGameStats(data.gameStats);
      })
      .catch(() => setError("Failed to load profile stats."));
  }, [user?.username]);

  return (
    <>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      <Profile generalStats={generalStats} gameStats={gameStats} />
    </>
  );
}

export default ProfilePage;
