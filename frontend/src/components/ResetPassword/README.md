# ResetPassword Component

**Use case**: AUTH-03 — Reset Password

Two-step password reset flow: (1) enter username/email, (2) enter and confirm new password.

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onResetPassword(identifier, newPassword)` | `function → Promise` | Yes | Performs the reset. Reject with `Error` to display a message. |
| `onBackToLogin()` | `function` | No | Navigates back to login. |

## Usage

```jsx
import ResetPassword from './components/ResetPassword';

<ResetPassword
  onResetPassword={async (id, newPw) => { /* call reset API */ }}
  onBackToLogin={() => navigate('/login')}
/>
```
