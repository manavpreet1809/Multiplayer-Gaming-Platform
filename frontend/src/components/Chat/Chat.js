import React, { useState } from 'react';
import './Chat.css';

/**
 * Chat component (UC-07).
 *
 * Props:
 *   messages           – array of { id, sender, text, timestamp }
 *   onSendMessage(text)– called when the user submits a message
 *   context            – "lobby" | "global" (display label)
 */
function Chat({ messages = [], onSendMessage, context = 'global' }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSendMessage && onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="chat">
      <h3 className="chat-title">
        {context === 'lobby' ? 'Lobby Chat' : 'Global Chat'}
      </h3>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <p className="chat-empty">No messages yet.</p>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className="chat-message">
              <span className="chat-sender">{msg.sender}</span>
              <span className="chat-text">{msg.text}</span>
              {msg.timestamp && (
                <span className="chat-time">{msg.timestamp}</span>
              )}
            </div>
          ))
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message…"
          aria-label="Chat message"
        />
        <button className="chat-send" type="submit">
          Send
        </button>
      </form>
    </div>
  );
}

export default Chat;
