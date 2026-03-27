import React from 'react';
import Login from './components/Login';
import Register from './components/Register';
import ResetPassword from './components/ResetPassword';
import Dashboard from './components/Dashboard';
import GameList from './components/GameList';
import GameLobby from './components/GameLobby';
import Chat from './components/Chat';
import Profile from './components/Profile';
import Leaderboard from './components/Leaderboard';
import GameResults from './components/GameResults';
import TicTacToeBoard from './components/TicTacToeBoard';
import ChessBoard from './components/ChessBoard';

const noop = () => {};
const asyncNoop = async () => {};

const sampleMessages = [
  { id: '1', sender: 'player1', text: 'Hey, ready to play?', timestamp: '12:00' },
  { id: '2', sender: 'player2', text: 'Yeah let\'s go!', timestamp: '12:01' },
  { id: '3', sender: 'player1', text: 'I\'ll go first', timestamp: '12:02' },
];

const sampleGames = [
  { id: 'chess', name: 'Chess', description: 'Classic two-player strategy board game.', playerCount: 42 },
  { id: 'ttt', name: 'Tic-Tac-Toe', description: 'Classic 3x3 grid game. First to three in a row wins.', playerCount: 18 },
];

const sampleRankings = [
  { rank: 1, username: 'grandmaster', tier: 'Gold', mmr: 1800, wins: 50, losses: 10 },
  { rank: 2, username: 'player1', tier: 'Silver', mmr: 1400, wins: 30, losses: 20 },
  { rank: 3, username: 'rookie', tier: 'Bronze', mmr: 900, wins: 10, losses: 15 },
];

const sampleGameStats = [
  { gameType: 'Chess', gamesPlayed: 7, wins: 4, losses: 3, rank: 'Silver', mmr: 1200 },
  { gameType: 'Tic-Tac-Toe', gamesPlayed: 3, wins: 2, losses: 0, rank: 'Gold', mmr: 1400 },
];

const sampleTttBoard = ['X', null, 'O', null, 'X', null, 'O', null, null];

function ScreenshotPage() {
  return (
    <div>
      {/* Each section is a screenshot target */}
      <div id="ss-login" style={{ minHeight: '100vh' }}>
        <Login onLogin={asyncNoop} onForgotPassword={noop} onRegister={noop} />
      </div>

      <div id="ss-register" style={{ minHeight: '100vh' }}>
        <Register onRegister={asyncNoop} onLogin={noop} />
      </div>

      <div id="ss-reset-password" style={{ minHeight: '100vh' }}>
        <ResetPassword onResetPassword={asyncNoop} onBackToLogin={noop} />
      </div>

      <div id="ss-dashboard" style={{ background: '#fff', padding: '1rem' }}>
        <Dashboard
          username="player1"
          status="idle"
          notifications={[{ id: '1', message: 'Game invite from player2' }]}
          onBrowseGames={noop}
          onCreateGame={noop}
          onJoinGame={noop}
          onEnqueue={noop}
          onOpenChat={noop}
          onViewProfile={noop}
          onLeaderboard={noop}
          onLogout={noop}
        />
      </div>

      <div id="ss-dashboard-ready" style={{ background: '#fff', padding: '1rem' }}>
        <Dashboard
          username="player1"
          status="game-ready"
          notifications={[]}
          onBrowseGames={noop}
          onCreateGame={noop}
          onJoinGame={noop}
          onEnqueue={noop}
          onOpenChat={noop}
          onJoinActiveGame={noop}
          onViewProfile={noop}
          onLeaderboard={noop}
          onLogout={noop}
        />
      </div>

      <div id="ss-game-list" style={{ background: '#fff', padding: '1rem' }}>
        <GameList
          games={sampleGames}
          selectedGameId="chess"
          onSelectGame={noop}
          onJoinLobby={noop}
          onBack={noop}
        />
      </div>

      <div id="ss-game-lobby" style={{ background: '#fff', padding: '1rem' }}>
        <GameLobby
          lobbyId="abc-1234"
          gameName="Chess"
          status="waiting"
          players={[
            { id: '1', username: 'player1', isReady: true },
            { id: '2', username: 'player2', isReady: false },
          ]}
          requiredPlayers={2}
          onLeaveLobby={noop}
          onToggleReady={noop}
          onStartGame={noop}
          chatComponent={
            <Chat messages={sampleMessages} onSendMessage={noop} context="lobby" />
          }
        />
      </div>

      <div id="ss-chat" style={{ background: '#fff', padding: '2rem', maxWidth: 500 }}>
        <Chat messages={sampleMessages} onSendMessage={noop} context="global" />
      </div>

      <div id="ss-profile" style={{ background: '#fff', padding: '1rem' }}>
        <Profile
          username="player1"
          email="player1@example.com"
          generalStats={{ gamesPlayed: 10, wins: 6, losses: 3, ties: 1 }}
          gameStats={sampleGameStats}
          onEditSettings={noop}
          onBack={noop}
        />
      </div>

      <div id="ss-leaderboard" style={{ background: '#fff', padding: '1rem' }}>
        <Leaderboard
          gameTypes={['Chess', 'Tic-Tac-Toe', 'Overall']}
          selectedGameType="Chess"
          onSelectGameType={noop}
          rankings={sampleRankings}
          currentUsername="player1"
          onBack={noop}
        />
      </div>

      <div id="ss-results-win" style={{ background: '#fff', padding: '1rem' }}>
        <GameResults
          result="win"
          winnerUsername="player1"
          mmrChange={25}
          newRank="Gold"
          onReturnDashboard={noop}
          onPlayAgain={noop}
          onViewLeaderboard={noop}
        />
      </div>

      <div id="ss-results-loss" style={{ background: '#fff', padding: '1rem' }}>
        <GameResults
          result="loss"
          winnerUsername="player2"
          mmrChange={-18}
          onReturnDashboard={noop}
          onPlayAgain={noop}
          onViewLeaderboard={noop}
        />
      </div>

      <div id="ss-results-draw" style={{ background: '#fff', padding: '1rem' }}>
        <GameResults
          result="draw"
          mmrChange={0}
          onReturnDashboard={noop}
          onPlayAgain={noop}
          onViewLeaderboard={noop}
        />
      </div>

      <div id="ss-tictactoe" style={{ background: '#fff', padding: '1rem' }}>
        <TicTacToeBoard
          board={sampleTttBoard}
          currentPlayer="X"
          isMyTurn={true}
          onCellClick={noop}
          playerSymbol="X"
          opponentName="player2"
        />
      </div>

      <div id="ss-tictactoe-win" style={{ background: '#fff', padding: '1rem' }}>
        <TicTacToeBoard
          board={['X', 'O', 'O', null, 'X', null, null, null, 'X']}
          winningCells={[0, 4, 8]}
          currentPlayer="X"
          isMyTurn={false}
          onCellClick={noop}
          playerSymbol="X"
          opponentName="player2"
        />
      </div>

      <div id="ss-chess" style={{ background: '#fff', padding: '1rem' }}>
        <ChessBoard
          currentPlayer="white"
          isMyTurn={true}
          onSquareClick={noop}
          playerColor="white"
          opponentName="player2"
        />
      </div>

      <div id="ss-chess-black" style={{ background: '#fff', padding: '1rem' }}>
        <ChessBoard
          currentPlayer="black"
          isMyTurn={false}
          onSquareClick={noop}
          playerColor="black"
          opponentName="player1"
          capturedByBlack={['P', 'P']}
          capturedByWhite={['p']}
        />
      </div>
    </div>
  );
}

export default ScreenshotPage;
