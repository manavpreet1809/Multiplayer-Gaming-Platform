import { useState } from "react";
import ErrorBoundary from "./components/ErrorBoundary";
import Login from "./components/Login";
import Register from "./components/Register";
import GameBoardDemo from "./components/GameBoardDemo";
import Dashboard from "./components/Dashboard";
import ScreenshotPage from "./ScreenshotPage";
import { useNavigate, Routes, Route } from "react-router-dom";
import { login as authLogin } from "./services/authService";
import "./App.css";
import ResetPassword from "./components/ResetPassword";

// Render screenshot page when ?screenshots is in the URL
const isScreenshotMode = new URLSearchParams(window.location.search).has(
  "screenshots",
);

function App() {
  const [view, setView] = useState("login");
  const navigate = useNavigate();

  if (isScreenshotMode) {
    return <ScreenshotPage />;
  }

  const handleLogin = async (identifier, password) => {
    await authLogin(identifier, password);
    navigate("/dashboard");
  };

  const handleForgotPassword = () => {
    // TODO: Navigate to reset-password view (AUTH-03)
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
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resetpassword" element={<ResetPassword />} />
      </Routes>
    </ErrorBoundary>
  );
}

export default App;
