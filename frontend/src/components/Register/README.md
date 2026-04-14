# Register Component

**Use case**: AUTH-01 / UC-02 — Create Account

Registration form with username, email, password, and confirm-password fields. Validates required fields, minimum password length (6 chars), and password match.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onRegister(username, email, password)` | `function → Promise` | Yes | Creates the account. Reject with `Error` to display a message. |
| `onLogin()` | `function` | No | Navigates to login. Link hidden if omitted. |

## Usage

```jsx
import Register from './components/Register';

<Register
  onRegister={async (user, email, pw) => { /* call registration API */ }}
  onLogin={() => navigate('/login')}
/>
```
