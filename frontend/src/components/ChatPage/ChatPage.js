import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Chat from '../Chat/Chat';
import { createGlobalChatWebSocket, sendGlobalChat } from '../../services/gameService';
import './ChatPage.css';

function ChatPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState('');
  const wsRef = useRef(null);
  const msgCounter = useRef(0);

  useEffect(() => {
    let mounted = true;

    (async () => {
      try {
        const ws = await createGlobalChatWebSocket(
          (msg) => {
            if (!mounted) return;
            if (msg.type === 'history') {
              setMessages(
                msg.messages.map((m) => ({
                  id: ++msgCounter.current,
                  sender: m.sender,
                  text: m.text,
                }))
              );
            } else if (msg.type === 'chat') {
              setMessages((prev) => [
                ...prev,
                { id: ++msgCounter.current, sender: msg.sender, text: msg.text },
              ]);
            }
          },
          () => { if (mounted) setConnected(true); },
          () => { if (mounted) setConnected(false); },
          () => {
            if (mounted) {
              setConnected(false);
              setError('Could not connect to chat. Make sure the server is running.');
            }
          },
        );

        if (!mounted) {
          ws.close();
          return;
        }
        wsRef.current = ws;
      } catch (err) {
        if (mounted) setError(err.message || 'Could not connect to chat.');
      }
    })();

    return () => {
      mounted = false;
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const handleSend = (text) => {
    sendGlobalChat(wsRef.current, text);
  };

  return (
    <div className="chat-page">
      <div className="chat-page-header">
        <h2>Global Chat</h2>
        <div className="chat-page-header-right">
          <span className={`chat-page-status ${connected ? 'chat-page-status--online' : ''}`}>
            {connected ? 'Connected' : 'Connecting…'}
          </span>
          <button className="chat-page-back" onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </button>
        </div>
      </div>

      {error && <p className="chat-page-error">{error}</p>}

      <div className="chat-page-body">
        <Chat messages={messages} onSendMessage={handleSend} context="global" />
      </div>
    </div>
  );
}

export default ChatPage;
