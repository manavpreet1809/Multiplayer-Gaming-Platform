/**
 * Validate a password against the same rules enforced by the backend
 * (schemas/auth.py PASSWORD_RULES).
 *
 * @param {string} password
 * @returns {string[]} array of failure messages (empty = valid)
 */
export default function validatePassword(password) {
  const errors = [];
  if (password.length < 8) errors.push('at least 8 characters');
  if (!/[A-Z]/.test(password)) errors.push('an uppercase letter');
  if (!/[a-z]/.test(password)) errors.push('a lowercase letter');
  if (!/\d/.test(password)) errors.push('a digit');
  if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?`~]/.test(password)) errors.push('a special character');
  return errors;
}
