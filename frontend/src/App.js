import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import ErrorBoundary from "./components/ErrorBoundary";
import Login from "./components/Login";
import Register from "./components/Register";
import ProfilePage from "./components/Profile/ProfilePage";
import ProtectedRoute from "./components/ProtectedRoute";
import GameBoardDemo from "./components/GameBoardDemo";
import DashboardPage from "./components/DashboardPage/DashboardPage";
import BrowseGamesPage from "./components/BrowseGamesPage/BrowseGamesPage";
import CreateGamePage from "./components/CreateGamePage/CreateGamePage";
import JoinGamePage from "./components/JoinGamePage/JoinGamePage";
import MatchmakePage from "./components/MatchmakePage/MatchmakePage";
import LobbyPage from "./components/LobbyPage/LobbyPage";
import GamePage from "./components/GamePage/GamePage";
import ChatPage from "./components/ChatPage/ChatPage";
import ScreenshotPage from "./ScreenshotPage";
import { useNavigate, Routes, Route } from "react-router-dom";
import { login as authLogin, getMe } from "./services/authService";
import "./App.css";
import ResetPassword from "./components/ResetPassword";
import LeaderboardPage from "./components/Leaderboard/LeaderboardPage";

// Render screenshot page when ?screenshots is in the URL
const isScreenshotMode = new URLSearchParams(window.location.search).has(
  "screenshots",
);

function App() {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  if (isScreenshotMode) {
    return <ScreenshotPage />;
  }

  const handleLogin = async (identifier, password) => {
    await authLogin(identifier, password);
    const user = await getMe();

    login(user);
    navigate("/dashboard");
  };

  const handleForgotPassword = () => {
    navigate("/resetpassword");
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <ErrorBoundary>
      <Routes>
        <Route
          path="/"
          element={
            <Login
              onLogin={handleLogin}
              onForgotPassword={handleForgotPassword}
              onRegister={handleRegister}
            />
          }
        />
        <Route path="/register" element={<Register />} />
        <Route path="/demo" element={<GameBoardDemo />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/browse"
          element={
            <ProtectedRoute>
              <BrowseGamesPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create-game"
          element={
            <ProtectedRoute>
              <CreateGamePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/join-game"
          element={
            <ProtectedRoute>
              <JoinGamePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/matchmake"
          element={
            <ProtectedRoute>
              <MatchmakePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lobby/:gameId"
          element={
            <ProtectedRoute>
              <LobbyPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/game/:gameId"
          element={
            <ProtectedRoute>
              <GamePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/leaderboard"
          element={
            <ProtectedRoute>
              <LeaderboardPage />
            </ProtectedRoute>
          }
        />
        <Route path="/resetpassword" element={<ResetPassword />} />
      </Routes>
    </ErrorBoundary>
  );
}

export default App;
