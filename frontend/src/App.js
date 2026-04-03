import { useState, useContext } from "react";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import ErrorBoundary from "./components/ErrorBoundary";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import ProtectedRoute from "./components/ProtectedRoute";
import GameBoardDemo from "./components/GameBoardDemo";
import Dashboard from "./components/Dashboard";
import ScreenshotPage from "./ScreenshotPage";
import { useNavigate, Routes, Route } from "react-router-dom";
import { login as authLogin } from "./services/authService";
import { getMe } from "./services/authService";
import "./App.css";
import ResetPassword from "./components/ResetPassword";
import Leaderboard from "./components/Leaderboard";

// Render screenshot page when ?screenshots is in the URL
const isScreenshotMode = new URLSearchParams(window.location.search).has(
  "screenshots",
);

function App() {
  const [view, setView] = useState("login");
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  if (isScreenshotMode) {
    return <ScreenshotPage />;
  }

  const handleLogin = async (identifier, password) => {
    const data = await authLogin(identifier, password);
    const user = await getMe();

    login(user);
    console.log(user);
    navigate("/dashboard");
  };

  const handleForgotPassword = () => {
    navigate("/resetpassword");
  };

  const handleRegister = () => {
    navigate("/register");
  };

  if (view === "demo") {
    return (
      <ErrorBoundary>
        <GameBoardDemo />
      </ErrorBoundary>
    );
  }

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
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/leaderboard"
          element={
            <ProtectedRoute>
              <Leaderboard gameTypes={["Chess", " TicTacToe"]} />
            </ProtectedRoute>
          }
        />
        <Route path="/resetpassword" element={<ResetPassword />} />
      </Routes>
    </ErrorBoundary>
  );
}

export default App;
