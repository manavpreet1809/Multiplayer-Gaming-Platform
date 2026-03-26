// import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { useState } from 'react';
// import Login from './components/Login';
import GameBoardDemo from './components/GameBoardDemo';
import ScreenshotPage from './ScreenshotPage';
import './App.css';
import './index.css';

// Render screenshot page when ?screenshots is in the URL
const isScreenshotMode = new URLSearchParams(window.location.search).has('screenshots');

function App() {
    const [view, setView] = useState('login');

    if (isScreenshotMode) {
        return <ScreenshotPage />;
    }

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
        /* <Login
           onLogin={handleLogin}
           onForgotPassword={handleForgotPassword}
           onRegister={handleRegister}
         />
         */
        <Dashboard />
    );
}

export default App;
