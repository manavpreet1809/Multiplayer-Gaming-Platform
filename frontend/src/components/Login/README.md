# Login Component

**Use case**: AUTH-02 / UC-03 — Log In

Provides a username/email + password form with error handling, loading state, and navigation links to Register and Forgot Password views.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onLogin(identifier, password)` | `function → Promise` | Yes | Authenticates the user. Reject with `Error` to display a message. |
| `onForgotPassword()` | `function` | No | Navigates to reset password. Link hidden if omitted. |
| `onRegister()` | `function` | No | Navigates to registration. Link hidden if omitted. |

## Usage

```jsx
import Login from './components/Login';

<Login
  onLogin={async (id, pw) => { /* call auth API */ }}
  onForgotPassword={() => navigate('/reset-password')}
  onRegister={() => navigate('/register')}
/>
```

## Tests

9 test cases in `Login.test.js` covering rendering, validation, submission, error display, and navigation links.
