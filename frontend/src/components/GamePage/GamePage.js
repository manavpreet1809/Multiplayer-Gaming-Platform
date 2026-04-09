import { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import ChessBoard from '../ChessBoard/ChessBoard';
import TicTacToeBoard from '../TicTacToeBoard/TicTacToeBoard';
import GameResults from '../GameResults/GameResults';
import Chat from '../Chat/Chat';
import {
  getGame,
  leaveGame,
  createGameWebSocket,
  sendMove,
  sendGameChat,
} from '../../services/gameService';
import { buildChessMove, buildTttMove, chessStateToProps, tttStateToProps, endResultToProps } from '../../adapters/gameAdapters';
import './GamePage.css';

function GamePage() {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  // Core state
  const [gameType, setGameType] = useState(null);
  const [engineState, setEngineState] = useState(null);
  const [playerColor, setPlayerColor] = useState(null);   // chess: "white"|"black"
  const [playerSymbol, setPlayerSymbol] = useState(null); // ttt: "X"|"O"
  const [endResult, setEndResult] = useState(null);
  const [error, setError] = useState('');

  // Chess interaction state
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [lastMove, setLastMove] = useState(null);

  // In-game chat
  const [chatMessages, setChatMessages] = useState([]);
  const [chatOpen, setChatOpen] = useState(false);
  const msgCounter = useRef(0);

  const wsRef = useRef(null);

  // ---- Determine this client's color/symbol from state ----
  const resolveIdentity = (state, type, username) => {
    const inferredType = type || (state?.activeColor ? 'chess' : state?.currentPlayer ? 'tictactoe' : null);
    const players = state?.players || {};

    if (!username) return {};

    if (inferredType === 'chess') {
      if (players.white === username) return { playerColor: 'white' };
      if (players.black === username) return { playerColor: 'black' };
      return {};
    }

    if (inferredType === 'tictactoe') {
      // ttt: players map is {"X": username, "O": username}
      const sym = Object.entries(players).find(([, v]) => v === username)?.[0];
      return sym ? { playerSymbol: sym } : {};
    }

    return {};
  };

  useEffect(() => {
    let mounted = true;

    // Fetch initial game info to know the game type
    getGame(gameId)
      .then((data) => {
        if (!mounted) return;
        setGameType(data.game_type);
        if (data.state) {
          setEngineState(data.state);
          const id = resolveIdentity(data.state, data.game_type, user?.username);
          if (id.playerColor) setPlayerColor(id.playerColor);
          if (id.playerSymbol) setPlayerSymbol(id.playerSymbol);
        }
      })
      .catch((err) => {
        if (mounted) setError(err.message || 'Failed to load game');
      });

    // Connect WebSocket
    (async () => {
      try {
        const ws = await createGameWebSocket(
          gameId,
          (msg) => {
            if (!mounted) return;

            if (msg.type === 'state') {
              const state = msg.state;
              setEngineState(state);
              const inferredType = state?.activeColor ? 'chess' : state?.currentPlayer ? 'tictactoe' : null;
              if (inferredType && !gameType) setGameType(inferredType);

              const id = resolveIdentity(state, inferredType, user?.username);
              if (id.playerColor) setPlayerColor(id.playerColor);
              if (id.playerSymbol) setPlayerSymbol(id.playerSymbol);
              if (msg.status === 'checkmate') {
                setError('Checkmate');
              } else if (msg.status === 'check') {
                setError('Check');
              } else if (!msg.result) {
                setError('');
              }
              if (msg.result) setEndResult(msg.result);
            } else if (msg.type === 'game_over') {
              setEndResult(msg.result);
            } else if (msg.type === 'chat') {
              setChatMessages((prev) => [
                ...prev,
                { id: ++msgCounter.current, sender: msg.sender, text: msg.text },
              ]);
            } else if (msg.type === 'error') {
              if (msg.error === 'checkmate') {
                setError('Checkmate');
              } else if (msg.error === 'check') {
                setError('Check');
              } else {
                setError(msg.error);
              }
              setSelectedSquare(null);
            }
          },
          undefined,
          () => { /* ws closed — could show reconnect banner */ },
        );

        if (!mounted) {
          ws.close();
          return;
        }
        wsRef.current = ws;
      } catch (err) {
        if (mounted) setError(err.message || 'Failed to connect to game socket');
      }
    })();

    return () => {
      mounted = false;
      if (wsRef.current) wsRef.current.close();
    };
  }, [gameId, user?.username]);

  // ---- Chess square click handler ----
  const handleChessSquareClick = (row, col) => {
    if (!engineState || endResult) return;

    const pieceAt = engineState?.board?.[row]?.[col] || null;
    const isOwnPiece =
      !!pieceAt &&
      ((playerColor === 'white' && pieceAt === pieceAt.toUpperCase()) ||
        (playerColor === 'black' && pieceAt === pieceAt.toLowerCase()));

    // If no square selected yet, select this one
    if (!selectedSquare) {
      if (!isOwnPiece) return;
      setSelectedSquare({ row, col });
      return;
    }

    // If clicked the same square, deselect
    if (selectedSquare.row === row && selectedSquare.col === col) {
      setSelectedSquare(null);
      return;
    }

    // Clicking another of your own pieces changes selection instead of attempting a move.
    if (isOwnPiece) {
      setSelectedSquare({ row, col });
      return;
    }

    // Submit move: from selectedSquare to clicked square
    const move = buildChessMove(
      { row: selectedSquare.row, col: selectedSquare.col },
      { row, col },
    );
    sendMove(wsRef.current, move);
    setSelectedSquare(null);
  };

  // ---- TicTacToe cell click handler ----
  const handleTttCellClick = (index) => {
    if (!engineState || endResult) return;
    sendMove(wsRef.current, buildTttMove(index));
  };

  const handleReturnDashboard = async () => {
    try { await leaveGame(gameId); } catch { /* best effort */ }
    navigate('/dashboard');
  };

  const handlePlayAgain = async () => {
    try { await leaveGame(gameId); } catch { /* best effort */ }
    navigate('/matchmake');
  };

  // ---- Render ----
  if (!engineState) {
    return (
      <div className="game-page-loading">
        {error ? <p className="game-page-error">{error}</p> : <p>Connecting to game…</p>}
      </div>
    );
  }

  const localPlayer = gameType === 'chess' ? playerColor : playerSymbol;
  const resultProps = endResultToProps(endResult, localPlayer, engineState?.players || {});

  return (
    <div className="game-page">
      {error && (
        <p className="game-page-error game-page-error--inline">{error}</p>
      )}

      {resultProps ? (
        <div className="game-page-results">
          <GameResults
            {...resultProps}
            onReturnDashboard={handleReturnDashboard}
            onPlayAgain={handlePlayAgain}
            onViewLeaderboard={() => navigate('/leaderboard')}
          />
        </div>
      ) : gameType === 'chess' && playerColor ? (
        <ChessBoard
          {...chessStateToProps(engineState, playerColor, {
            selectedSquare,
            lastMove,
          })}
          onSquareClick={handleChessSquareClick}
        />
      ) : gameType === 'tictactoe' && playerSymbol ? (
        <TicTacToeBoard
          {...tttStateToProps(engineState, playerSymbol)}
          onCellClick={handleTttCellClick}
        />
      ) : (
        <p className="game-page-loading">Waiting for game state…</p>
      )}

      {/* In-game chat toggle */}
      <div className="game-page-chat-container">
        <button
          className="game-page-chat-toggle"
          onClick={() => setChatOpen((o) => !o)}
        >
          {chatOpen ? 'Close Chat' : 'Chat'}
          {!chatOpen && chatMessages.length > 0 && (
            <span className="game-page-chat-badge">{chatMessages.length}</span>
          )}
        </button>
        {chatOpen && (
          <div className="game-page-chat-panel">
            <Chat
              messages={chatMessages}
              onSendMessage={(text) => sendGameChat(wsRef.current, text)}
              context="lobby"
            />
          </div>
        )}
      </div>

      {!resultProps && (
        <div className="game-page-footer">
          <button className="game-page-leave" onClick={handleReturnDashboard}>
            Forfeit &amp; Leave
          </button>
        </div>
      )}
    </div>
  );
}

export default GamePage;
