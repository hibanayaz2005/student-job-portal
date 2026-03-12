import React, { useState } from 'react';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'student'
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Login attempt with email: ${formData.email}, role: ${formData.role}. This will connect to the backend API.`);
  };

  return (
    <div className="login-container" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--surface)' }}>
      <div className="login-card" style={{ background: 'white', padding: '40px', borderRadius: '20px', boxShadow: '0 10px 40px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <h2 style={{ fontFamily: 'var(--font-head)', fontSize: '28px', fontWeight: '700', marginBottom: '10px' }}>
            Welcome Back
          </h2>
          <p style={{ color: 'var(--muted)', fontSize: '16px' }}>
            Sign in to your CareerBridge account
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
              Email Address
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              style={{ width: '100%', padding: '12px 16px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '14px' }}
              placeholder="your@email.com"
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
              Password
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={{ width: '100%', padding: '12px 16px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '14px' }}
              placeholder="••••••••"
            />
          </div>

          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
              I am a
            </label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              style={{ width: '100%', padding: '12px 16px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '14px' }}
            >
              <option value="student">Student</option>
              <option value="employer">Employer</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button
            type="submit"
            style={{ width: '100%', padding: '14px', background: 'var(--accent)', color: 'white', border: 'none', borderRadius: '8px', fontSize: '16px', fontWeight: '600', cursor: 'pointer', marginBottom: '15px' }}
          >
            Sign In
          </button>
        </form>

        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ color: 'var(--muted)', fontSize: '14px', marginBottom: '15px' }}>OR</div>
          <button
            onClick={() => alert('Google OAuth will be implemented here')}
            style={{ width: '100%', padding: '12px', background: 'white', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '14px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
          >
            <span>🔗</span> Continue with Google
          </button>
        </div>

        <div style={{ textAlign: 'center', fontSize: '14px', color: 'var(--muted)' }}>
          Don't have an account? <a href="#register" style={{ color: 'var(--accent)', textDecoration: 'none' }}>Sign up</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
