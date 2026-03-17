# Chat Component

**Use case**: UC-07 — Chat

Scrollable message panel with a text input. Can be used standalone or embedded inside GameLobby. Prevents sending empty messages.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `messages` | `[{ id, sender, text, timestamp }]` | No | Chat messages (default: `[]`) |
| `onSendMessage(text)` | `function` | No | Called when a message is submitted |
| `context` | `"lobby" \| "global"` | No | Display label (default: `"global"`) |

## Usage

```jsx
import Chat from './components/Chat';

<Chat
  messages={[{ id: '1', sender: 'player1', text: 'Hello!', timestamp: '12:00' }]}
  onSendMessage={(text) => sendMessage(text)}
  context="lobby"
/>
```
