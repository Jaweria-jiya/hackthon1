import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/contexts/AuthContext';
import styles from './signup.module.css'; // Assuming a CSS module for styling

const Signup = () => {
  const { signup, loading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState<'Beginner' | 'Intermediate' | 'Advanced'>('Beginner');
  const [hardwareBackground, setHardwareBackground] = useState<'None' | 'Basic' | 'Advanced'>('None');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const success = await signup(email, password, { softwareBackground, hardwareBackground });
      if (success) {
        // Redirect to book content after successful signup and auto-login
        window.location.href = '/docs/intro'; // Assuming '/docs/intro' is the main book content page
      } else {
        setError('Signup failed. Please try again.');
      }
    } catch (err) {
      setError('An unexpected error occurred during signup.');
      console.error(err);
    }
  };

  return (
    <Layout title="Sign Up" description="Sign up for an account">
      <div className={styles.signupContainer}>
        <h2>Sign Up</h2>
        {error && <div className={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit} className={styles.signupForm}>
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
          <div className={styles.formGroup}>
            <label htmlFor="softwareBackground">Software Background</label>
            <select
              id="softwareBackground"
              value={softwareBackground}
              onChange={(e) => setSoftwareBackground(e.target.value as 'Beginner' | 'Intermediate' | 'Advanced')}
              className={styles.selectField}
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="hardwareBackground">Hardware Background</label>
            <select
              id="hardwareBackground"
              value={hardwareBackground}
              onChange={(e) => setHardwareBackground(e.target.value as 'None' | 'Basic' | 'Advanced')}
              className={styles.selectField}
            >
              <option value="None">None</option>
              <option value="Basic">Basic</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className={styles.submitButton}>
            {loading ? 'Signing Up...' : 'Sign Up'}
          </button>
        </form>
        <div className={styles.oauthOptions}>
          {/* OAuth options will be added to the Signin page */}
          <p>Already have an account? <a href="/signin">Sign In</a></p>
        </div>
      </div>
    </Layout>
  );
};

export default Signup;
