import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createGame } from '../../services/gameService';
import './CreateGamePage.css';

function CreateGamePage() {
  const navigate = useNavigate();
  const [gameType, setGameType] = useState('chess');
  const [visibility, setVisibility] = useState('public');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const game = await createGame(gameType, visibility);
      navigate(`/lobby/${game.game_id}`);
    } catch (err) {
      setError(err.message || 'Failed to create game');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-game-page">
      <div className="create-game-card">
        <div className="create-game-header">
          <h2>Create Game</h2>
          <button className="create-game-back" onClick={() => navigate('/dashboard')}>
            Back
          </button>
        </div>

        {error && <p className="create-game-error">{error}</p>}

        <form onSubmit={handleSubmit} className="create-game-form">
          <div className="create-game-field">
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

          <div className="create-game-field">
            <label htmlFor="visibility">Visibility</label>
            <select
              id="visibility"
              value={visibility}
              onChange={(e) => setVisibility(e.target.value)}
            >
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>

          <button
            type="submit"
            className="create-game-submit"
            disabled={loading}
          >
            {loading ? 'Creating…' : 'Create Lobby'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateGamePage;
