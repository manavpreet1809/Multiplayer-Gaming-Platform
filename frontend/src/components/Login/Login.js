import React, { useState } from "react";
import "./Login.css";
import { register as authRegister } from "../../services/authService";

/**
 * Reusable Login component (AUTH-02).
 *
 * Props:
 *   onLogin(identifier, password)  – called on form submit; should return a promise
 *                                     that resolves on success or rejects/throws with
 *                                     an error message string.
 *   onForgotPassword()             – navigates to the reset-password view.
 *   onRegister()                   – navigates to the registration view.
 */
function Login({ onLogin, onForgotPassword, onRegister }) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!identifier.trim() || !password) {
      setError("Please enter your username/email and password.");
      return;
    }

    setLoading(true);
    try {
      await onLogin(identifier.trim(), password);
    } catch (err) {
      setError(err?.message || "Invalid credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit} noValidate>
        <h2 className="login-title">Log In</h2>

        {error && (
          <div className="login-error" role="alert">
            {error}
          </div>
        )}

        <label className="login-label" htmlFor="login-identifier">
          Username or Email
        </label>
        <input
          id="login-identifier"
          className="login-input"
          type="text"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="Enter username or email"
          autoComplete="username"
          disabled={loading}
        />

        <label className="login-label" htmlFor="login-password">
          Password
        </label>
        <input
          id="login-password"
          className="login-input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter password"
          autoComplete="current-password"
          disabled={loading}
        />

        <button className="login-button" type="submit" disabled={loading}>
          {loading ? "Logging in…" : "Log In"}
        </button>

        <div className="login-links">
          {onForgotPassword && (
            <button
              type="button"
              className="login-link"
              onClick={onForgotPassword}
              disabled={loading}
            >
              Forgot password?
            </button>
          )}
          {onRegister && (
            <button
              type="button"
              className="login-link"
              onClick={onRegister}
              disabled={loading}
            >
              Create an account
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default Login;
