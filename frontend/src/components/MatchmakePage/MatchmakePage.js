import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { matchmake } from '../../services/gameService';
import './MatchmakePage.css';

function MatchmakePage() {
  const navigate = useNavigate();
  const [gameType, setGameType] = useState('chess');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFind = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const game = await matchmake(gameType);
      navigate(`/lobby/${game.game_id}`);
    } catch (err) {
      setError(err.message || 'Matchmaking failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="matchmake-page">
      <div className="matchmake-card">
        <div className="matchmake-header">
          <h2>Find a Match</h2>
          <button className="matchmake-back" onClick={() => navigate('/dashboard')}>
            Back
          </button>
        </div>

        {error && <p className="matchmake-error">{error}</p>}

        <form onSubmit={handleFind} className="matchmake-form">
          <div className="matchmake-field">
            <label htmlFor="gameType">Game Type</label>
            <select
              id="gameType"
              value={gameType}
              onChange={(e) => setGameType(e.target.value)}
            >
              <option value="chess">Chess</option>
              <option value="tictactoe">Tic-Tac-Toe</option>
            </select>
          </div>
          <button type="submit" className="matchmake-submit" disabled={loading}>
            {loading ? 'Searching…' : 'Find Match'}
          </button>
        </form>

        <p className="matchmake-hint">
          We&apos;ll join you to an open lobby, or create a new one if none is available.
        </p>
      </div>
    </div>
  );
}

export default MatchmakePage;
