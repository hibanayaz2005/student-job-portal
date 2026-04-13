import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ scrollY }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  useEffect(() => {
    setIsScrolled(scrollY > 50);
  }, [scrollY]);
  
  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };
  
  const handleNavClick = (section) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(section);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };
  return (
    <nav className={isScrolled ? 'scrolled' : ''}>
      <div className="logo">
        <span className="logo-text">Career</span>
        <span className="logo-accent">Bridge</span>
      </div>
      
      {/* Desktop Navigation */}
      <div className="nav-links desktop-nav">
        <button 
          onClick={() => handleNavClick('how')}
          className="nav-link"
        >
          How it Works
          <span className="nav-underline"></span>
        </button>
        <button 
          onClick={() => handleNavClick('jobs')}
          className="nav-link"
        >
          Jobs
          <span className="nav-underline"></span>
        </button>
        <button 
          onClick={() => handleNavClick('courses')}
          className="nav-link"
        >
          Courses
          <span className="nav-underline"></span>
        </button>
        <button 
          onClick={() => handleNavClick('mentorship')}
          className="nav-link"
        >
          Mentorship
          <span className="nav-underline"></span>
        </button>
        <button 
          onClick={() => handleNavClick('resume')}
          className="nav-link"
        >
          Resume AI
          <span className="nav-underline"></span>
        </button>
      </div>
      
      {/* Mobile Menu Toggle */}
      <button 
        className="mobile-menu-toggle"
        onClick={toggleMobileMenu}
        aria-label="Toggle menu"
      >
        <span className={`hamburger ${mobileMenuOpen ? 'open' : ''}`}>
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>
      
      {/* CTA Buttons */}
      <div className="nav-actions">
        <Link to="/login" className="nav-cta-secondary">
          <span>Sign In</span>
          <div className="cta-glow"></div>
        </Link>
        <Link to="/register" className="nav-cta">
          <span>Get Started</span>
          <div className="cta-shine"></div>
        </Link>
      </div>
      
      {/* Mobile Menu */}
      <div className={`mobile-nav ${mobileMenuOpen ? 'open' : ''}`}>
        <button 
          onClick={() => handleNavClick('how')}
          className="mobile-nav-link"
        >
          How it Works
        </button>
        <button 
          onClick={() => handleNavClick('jobs')}
          className="mobile-nav-link"
        >
          Jobs
        </button>
        <button 
          onClick={() => handleNavClick('courses')}
          className="mobile-nav-link"
        >
          Courses
        </button>
        <button 
          onClick={() => handleNavClick('mentorship')}
          className="mobile-nav-link"
        >
          Mentorship
        </button>
        <button 
          onClick={() => handleNavClick('resume')}
          className="mobile-nav-link"
        >
          Resume AI
        </button>
      </div>
    </nav>
  );
};

export default Navbar;