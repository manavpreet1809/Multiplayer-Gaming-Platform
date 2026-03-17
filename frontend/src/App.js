import { useState } from 'react';
import Login from './components/Login';
import GameBoardDemo from './components/GameBoardDemo';
import './App.css';

function App() {
  const [view, setView] = useState('login');

  const handleLogin = async (identifier, password) => {
    // TODO: Replace with real authentication logic (User Store Stub lookup)
    console.log('Login attempt:', identifier);
    // For demo purposes, any login goes to the board demo
    setView('demo');
  };

  const handleForgotPassword = () => {
    // TODO: Navigate to reset-password view (AUTH-03)
    console.log('Navigate to forgot password');
  };

  const handleRegister = () => {
    // TODO: Navigate to registration view (AUTH-01)
    console.log('Navigate to register');
  };

  if (view === 'demo') {
    return <GameBoardDemo />;
  }

  return (
    <Login
      onLogin={handleLogin}
      onForgotPassword={handleForgotPassword}
      onRegister={handleRegister}
    />
  );
}

export default App;
