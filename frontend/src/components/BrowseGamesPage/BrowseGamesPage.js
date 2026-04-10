import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GameList from '../GameList/GameList';
import { matchmake } from '../../services/gameService';
import './BrowseGamesPage.css';

const GAME_TYPES = [
  {
    id: 'chess',
    name: 'Chess',
    description: 'Classic two-player strategy game on an 8x8 board.',
    playerCount: 2,
  },
  {
    id: 'tictactoe',
    name: 'Tic-Tac-Toe',
    description: 'Simple but fun 3x3 grid game. First to get three in a row wins.',
    playerCount: 2,
  },
];

function BrowseGamesPage() {
  const navigate = useNavigate();
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleJoinLobby = async (gameTypeId) => {
    setLoading(true);
    setError('');
    try {
      const game = await matchmake(gameTypeId);
      navigate(`/lobby/${game.game_id}`);
    } catch (err) {
      setError(err.message || 'Failed to join lobby');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="browse-games-page">
      {error && <p className="browse-games-error">{error}</p>}
      {loading && <p className="browse-games-loading">Finding a lobby…</p>}
      <GameList
        games={GAME_TYPES}
        selectedGameId={selected}
        onSelectGame={setSelected}
        onJoinLobby={handleJoinLobby}
        onBack={() => navigate('/dashboard')}
      />
    </div>
  );
}

export default BrowseGamesPage;
