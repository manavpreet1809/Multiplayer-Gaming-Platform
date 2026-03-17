import Login from './components/Login';
import './App.css';

function App() {
  const handleLogin = async (identifier, password) => {
    // TODO: Replace with real authentication logic (User Store Stub lookup)
    console.log('Login attempt:', identifier);
    throw new Error('Authentication not yet implemented.');
  };

  const handleForgotPassword = () => {
    // TODO: Navigate to reset-password view (AUTH-03)
    console.log('Navigate to forgot password');
  };

  const handleRegister = () => {
    // TODO: Navigate to registration view (AUTH-01)
    console.log('Navigate to register');
  };

  return (
    <Login
      onLogin={handleLogin}
      onForgotPassword={handleForgotPassword}
      onRegister={handleRegister}
    />
  );
}

export default App;
