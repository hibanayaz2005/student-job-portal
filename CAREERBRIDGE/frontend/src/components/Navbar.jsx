import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <div className="logo">Career<span>Bridge</span></div>
      <div className="nav-links">
        <a href="#how">How it Works</a>
        <a href="#jobs">Jobs</a>
        <a href="#courses">Courses</a>
        <a href="#mentorship">Mentorship</a>
        <a href="#resume">Resume AI</a>
      </div>
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        <Link to="/login" className="nav-cta-secondary" style={{ 
          padding: '8px 16px', 
          background: 'transparent', 
          color: 'var(--accent)', 
          border: '1px solid var(--accent)', 
          borderRadius: '6px', 
          textDecoration: 'none',
          fontSize: '14px',
          fontWeight: '600'
        }}>
          Sign In
        </Link>
        <Link to="/register" className="nav-cta" style={{
          padding: '8px 16px',
          background: 'var(--accent)',
          color: 'white',
          borderRadius: '6px',
          textDecoration: 'none',
          fontSize: '14px',
          fontWeight: '600'
        }}>
          Get Started →
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;