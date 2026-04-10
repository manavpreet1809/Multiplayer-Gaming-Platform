import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import {
  register as authRegister,
  login as authLogin,
  getMe,
} from "../../services/authService";
import { AuthContext } from "../../context/AuthContext";
import validatePassword from "../../utils/validatePassword";
import "./Register.css";

/**
 * Register component (UC-02 / AUTH-01).
 *
 * Props:
 *   onRegister(username, email, password) – returns a promise
 *   onLogin()                             – navigate to login view
 */
function Register({ onRegister, onLogin }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username.trim() || !email.trim() || !password) {
      setError("All fields are required.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const pwdErrors = validatePassword(password);
    if (pwdErrors.length > 0) {
      setError("Password must contain " + pwdErrors.join(", ") + ".");
      return;
    }

    setLoading(true);
    try {
      await authRegister(username.trim(), email.trim(), password);
      const tokenData = await authLogin(username.trim(), password);
      const user = await getMe();
      login(user);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.message || "Unable to create account, please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit} noValidate>
        <h2 className="register-title">Create Account</h2>

        {error && (
          <div className="register-error" role="alert">
            {error}
          </div>
        )}

        <label className="register-label" htmlFor="register-username">
          Username
        </label>
        <input
          id="register-username"
          className="register-input"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Choose a username"
          autoComplete="username"
          disabled={loading}
        />

        <label className="register-label" htmlFor="register-email">
          Email
        </label>
        <input
          id="register-email"
          className="register-input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          autoComplete="email"
          disabled={loading}
        />

        <label className="register-label" htmlFor="register-password">
          Password
        </label>
        <input
          id="register-password"
          className="register-input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Create a password"
          autoComplete="new-password"
          disabled={loading}
        />

        <label className="register-label" htmlFor="register-confirm-password">
          Confirm Password
        </label>
        <input
          id="register-confirm-password"
          className="register-input"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm your password"
          autoComplete="new-password"
          disabled={loading}
        />

        <button className="register-button" type="submit" disabled={loading}>
          {loading ? "Creating account…" : "Create Account"}
        </button>

        <div className="register-links">
          <button
            type="button"
            className="register-link"
            onClick={() => navigate("/")}
            disabled={loading}
          >
            Already have an account? Log in
          </button>
        </div>
      </form>
    </div>
  );
}

export default Register;
