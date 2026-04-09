import { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import GameLobby from '../GameLobby/GameLobby';
import Chat from '../Chat/Chat';
import {
  getGame,
  startGame,
  leaveGame,
  createGameWebSocket,
  sendGameChat,
} from '../../services/gameService';
import './LobbyPage.css';

function LobbyPage() {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const [lobby, setLobby] = useState(null);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');
  const [starting, setStarting] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef(null);
  const msgCounter = useRef(0);

  useEffect(() => {
    let mounted = true;

    // 1. Fetch initial state via REST
    getGame(gameId)
      .then((data) => {
        if (mounted) setLobby(data);
      })
      .catch((err) => {
        if (mounted) setError(err.message || 'Failed to load lobby');
      });

    // 2. Connect WebSocket for live updates
    (async () => {
      try {
        const ws = await createGameWebSocket(
          gameId,
          (msg) => {
            if (!mounted) return;
            if (msg.type === 'lobby') {
              setLobby(msg.data);
            } else if (msg.type === 'player_joined' || msg.type === 'player_left') {
              setLobby((prev) =>
                prev ? { ...prev, player_ids: msg.players, host_id: msg.host_id ?? prev.host_id } : prev
              );
            } else if (msg.type === 'game_started') {
              navigate(`/game/${gameId}`);
            } else if (msg.type === 'chat') {
              setMessages((prev) => [
                ...prev,
                { id: ++msgCounter.current, sender: msg.sender, text: msg.text },
              ]);
            } else if (msg.type === 'error') {
              setError(msg.error);
            }
          },
          () => setWsConnected(true),
          () => setWsConnected(false),
          () => setWsConnected(false),
        );

        if (!mounted) {
          ws.close();
          return;
        }
        wsRef.current = ws;
      } catch (err) {
        if (mounted) {
          setWsConnected(false);
          setError(err.message || 'Failed to connect to lobby updates');
        }
      }
    })();

    return () => {
      mounted = false;
      if (wsRef.current) wsRef.current.close();
    };
  }, [gameId, navigate]);

  // Polling fallback when WebSocket is not connected
  useEffect(() => {
    if (wsConnected) return;
    const id = setInterval(() => {
      getGame(gameId)
        .then((data) => {
          setLobby(data);
          if (data.status === 1) navigate(`/game/${gameId}`);
        })
        .catch(() => {});
    }, 3000);
    return () => clearInterval(id);
  }, [gameId, wsConnected, navigate]);

  const handleStart = async () => {
    setStarting(true);
    setError('');
    try {
      await startGame(gameId);
      navigate(`/game/${gameId}`);
    } catch (err) {
      setError(err.message || 'Failed to start game');
      setStarting(false);
    }
  };

  const handleLeave = async () => {
    try {
      await leaveGame(gameId);
    } catch { /* best-effort */ }
    navigate('/dashboard');
  };

  const handleSendChat = (text) => {
    sendGameChat(wsRef.current, text);
  };

  if (!lobby) {
    return (
      <div className="lobby-page-loading">
        {error ? <p className="lobby-page-error">{error}</p> : <p>Loading lobby…</p>}
      </div>
    );
  }

  const players = lobby.player_ids.map((id) => ({
    id,
    username: id,
    isReady: lobby.player_ids.length >= lobby.max_players,
  }));

  const isHost = user?.username === lobby.host_id;
  const gameTypeLabel = lobby.game_type === 'tictactoe' ? 'Tic-Tac-Toe' : 'Chess';

  return (
    <div className="lobby-page">
      {error && <p className="lobby-page-error">{error}</p>}
      {starting && <p className="lobby-page-info">Starting game…</p>}
      <div className="lobby-page-code">
        Lobby Code: <strong>{lobby.lobby_code}</strong>
      </div>
      <GameLobby
        lobbyId={lobby.lobby_code}
        gameName={gameTypeLabel}
        status={lobby.status === 1 ? 'started' : 'waiting'}
        players={players}
        requiredPlayers={lobby.max_players}
        onLeaveLobby={handleLeave}
        onStartGame={isHost ? handleStart : undefined}
        chatComponent={
          <Chat
            messages={messages}
            onSendMessage={handleSendChat}
            context="lobby"
          />
        }
      />
    </div>
  );
}

export default LobbyPage;
