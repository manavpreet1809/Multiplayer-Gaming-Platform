import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { getMe } from "../../services/authService";
import Profile from "./Profile";

function ProfilePage() {
  const { login } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const refreshProfile = async () => {
      try {
        const latestUser = await getMe();
        if (!mounted) return;
        login(latestUser);
      } catch (err) {
        if (!mounted) return;
        setError(err.message || "Failed to load profile.");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    refreshProfile();
    return () => {
      mounted = false;
    };
  }, [login]);

  if (loading) {
    return <div className="profile-loading">Loading profile…</div>;
  }

  if (error) {
    return <div className="profile-error">{error}</div>;
  }

  return <Profile />;
}

export default ProfilePage;
