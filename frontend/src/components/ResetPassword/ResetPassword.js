import React, { useState } from 'react';
import './ResetPassword.css';

/**
 * ResetPassword component (AUTH-03).
 *
 * Props:
 *   onResetPassword(identifier, newPassword) – returns a promise
 *   onBackToLogin()                          – navigate back to login
 */
function ResetPassword({ onResetPassword, onBackToLogin }) {
  const [step, setStep] = useState('identify'); // "identify" | "reset"
  const [identifier, setIdentifier] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleIdentify = (e) => {
    e.preventDefault();
    setError('');
    if (!identifier.trim()) {
      setError('Please enter your username or email.');
      return;
    }
    setStep('reset');
  };

  const handleReset = async (e) => {
    e.preventDefault();
    setError('');

    if (!newPassword) {
      setError('Please enter a new password.');
      return;
    }

    const pwdErrors = [];
    if (newPassword.length < 8) pwdErrors.push('at least 8 characters');
    if (!/[A-Z]/.test(newPassword)) pwdErrors.push('an uppercase letter');
    if (!/[a-z]/.test(newPassword)) pwdErrors.push('a lowercase letter');
    if (!/\d/.test(newPassword)) pwdErrors.push('a digit');
    if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?`~]/.test(newPassword)) pwdErrors.push('a special character');
    if (pwdErrors.length > 0) {
      setError('Password must contain ' + pwdErrors.join(', ') + '.');
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await onResetPassword(identifier.trim(), newPassword);
      setSuccess('Password has been reset. You can now log in.');
    } catch (err) {
      setError(err?.message || 'Unable to reset password, please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reset-container">
      <div className="reset-form-wrapper">
        <h2 className="reset-title">Reset Password</h2>

        {error && (
          <div className="reset-error" role="alert">
            {error}
          </div>
        )}

        {success ? (
          <div className="reset-success">
            <p>{success}</p>
            {onBackToLogin && (
              <button className="reset-button" onClick={onBackToLogin}>
                Back to Log In
              </button>
            )}
          </div>
        ) : step === 'identify' ? (
          <form onSubmit={handleIdentify} noValidate>
            <label className="reset-label" htmlFor="reset-identifier">
              Username or Email
            </label>
            <input
              id="reset-identifier"
              className="reset-input"
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="Enter your username or email"
              autoComplete="username"
            />
            <button className="reset-button" type="submit">
              Continue
            </button>
          </form>
        ) : (
          <form onSubmit={handleReset} noValidate>
            <p className="reset-info">
              Resetting password for <strong>{identifier}</strong>
            </p>

            <label className="reset-label" htmlFor="reset-new-password">
              New Password
            </label>
            <input
              id="reset-new-password"
              className="reset-input"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password"
              autoComplete="new-password"
              disabled={loading}
            />

            <label className="reset-label" htmlFor="reset-confirm-password">
              Confirm New Password
            </label>
            <input
              id="reset-confirm-password"
              className="reset-input"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
              autoComplete="new-password"
              disabled={loading}
            />

            <button className="reset-button" type="submit" disabled={loading}>
              {loading ? 'Resetting…' : 'Reset Password'}
            </button>
          </form>
        )}

        <div className="reset-links">
          {onBackToLogin && !success && (
            <button
              type="button"
              className="reset-link"
              onClick={onBackToLogin}
              disabled={loading}
            >
              Back to Log In
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;
