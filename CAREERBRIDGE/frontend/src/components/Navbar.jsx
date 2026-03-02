import React from 'react';

const Navbar = () => {
  return (
    <nav>
      <div className="logo">Career<span>Bridge</span></div>
      <div className="nav-links">
        <a href="#how">How it Works</a>
        <a href="#jobs">Jobs</a>
        <a href="#courses">Courses</a>
        <a href="#resume">Resume AI</a>
      </div>
      <a className="nav-cta" href="#verify">Get Verified →</a>
    </nav>
  );
};

export default Navbar;