import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/contexts/AuthContext';
import styles from './signin.module.css'; // Assuming a CSS module for styling

const Signin = () => {
  const { login, oauthLogin, loading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleEmailPasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const success = await login(email, password);
      if (success) {
        window.location.href = '/docs/intro'; // Redirect to book content after successful signin
      } else {
        setError('Login failed. Invalid email or password.');
      }
    } catch (err) {
      setError('An unexpected error occurred during login.');
      console.error(err);
    }
  };

  const handleOAuthLogin = async (provider: 'google' | 'github') => {
    setError(null);
    try {
      const success = await oauthLogin(provider);
      if (success) {
        window.location.href = '/docs/intro'; // Redirect to book content after successful signin
      } else {
        setError(`Login with ${provider} failed.`);
      }
    } catch (err) {
      setError(`An unexpected error occurred during ${provider} login.`);
      console.error(err);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={styles.signinContainer}>
        <h2>Sign In</h2>
        {error && <div className={styles.error}>{error}</div>}
        <form onSubmit={handleEmailPasswordSubmit} className={styles.signinForm}>
          <div className={styles.formGroup}>
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className={styles.inputField}
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className={styles.inputField}
            />
          </div>
          <button type="submit" disabled={loading} className={styles.submitButton}>
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>
        <div className={styles.oauthOptions}>
          <p>Or sign in with:</p>
          <button
            onClick={() => handleOAuthLogin('google')}
            disabled={loading}
            className={`${styles.oauthButton} ${styles.googleButton}`}
          >
            Sign in with Google
          </button>
          <button
            onClick={() => handleOAuthLogin('github')}
            disabled={loading}
            className={`${styles.oauthButton} ${styles.githubButton}`}
          >
            Sign in with GitHub
          </button>
        </div>
        <p className={styles.signupLink}>Don't have an account? <a href="/signup">Sign Up</a></p>
      </div>
    </Layout>
  );
};

export default Signin;
