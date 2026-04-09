import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { joinGameByCode } from '../../services/gameService';
import './JoinGamePage.css';

function JoinGamePage() {
  const navigate = useNavigate();
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim()) return;
    setLoading(true);
    setError('');
    try {
      const game = await joinGameByCode(code.trim().toUpperCase());
      navigate(`/lobby/${game.game_id}`);
    } catch (err) {
      setError(err.message || 'Lobby not found');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="join-game-page">
      <div className="join-game-card">
        <div className="join-game-header">
          <h2>Join Game</h2>
          <button className="join-game-back" onClick={() => navigate('/dashboard')}>
            Back
          </button>
        </div>

        {error && <p className="join-game-error">{error}</p>}

        <form onSubmit={handleSubmit} className="join-game-form">
          <div className="join-game-field">
            <label htmlFor="lobbyCode">Lobby Code</label>
            <input
              id="lobbyCode"
              type="text"
              maxLength={4}
              placeholder="ABCD"
              value={code}
              onChange={(e) => setCode(e.target.value.toUpperCase())}
              className="join-game-input"
              autoComplete="off"
            />
          </div>
          <button
            type="submit"
            className="join-game-submit"
            disabled={loading || code.length !== 4}
          >
            {loading ? 'Joining…' : 'Join Lobby'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default JoinGamePage;
