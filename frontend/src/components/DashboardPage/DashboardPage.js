import { useNavigate } from 'react-router-dom';
import Dashboard from '../Dashboard/Dashboard';

/**
 * Wires Dashboard display component to React Router navigation.
 * All action button handlers live here so Dashboard stays a pure display component.
 */
function DashboardPage() {
  const navigate = useNavigate();

  return (
    <Dashboard
      onBrowseGames={() => navigate('/browse')}
      onCreateGame={() => navigate('/create-game')}
      onJoinGame={() => navigate('/join-game')}
      onEnqueue={() => navigate('/matchmake')}
      onOpenChat={() => navigate('/chat')}
      onLeaderboard={() => navigate('/leaderboard')}
    />
  );
}

export default DashboardPage;
