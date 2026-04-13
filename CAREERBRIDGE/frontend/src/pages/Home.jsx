import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import HowItWorks from '../components/HowItWorks';
import Verification from '../components/Verification';
import JobCard from '../components/JobCard';
import Courses from '../components/Courses';
import ResumeScorer from '../components/ResumeScorer';
import DashboardPreview from '../components/DashboardPreview';
import MentorAvailability from '../components/MentorAvailability';
import TestMentorAPI from '../components/TestMentorAPI';

const Home = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const jobs = [
    { id: 1, title: "Frontend Developer Intern", company: "Zoho Corporation", location: "Chennai", type: "Internship", eligible_years: "3rd & Final Year", description: "React, JavaScript, CSS. Work on real products.", salary: "₹15K–20K/mo", is_new: true },
    { id: 2, title: "Cloud Support Associate", company: "AWS India", location: "Remote", type: "Full-time", eligible_years: "Final Year Only", description: "Entry-level cloud role. AWS training provided.", salary: "₹6–8 LPA", is_new: false }
  ];

  useEffect(() => {
    setIsLoaded(true);

    const handleScroll = () => setScrollY(window.scrollY);
    const handleMouseMove = (e) => setMousePosition({ x: e.clientX, y: e.clientY });

    window.addEventListener('scroll', handleScroll);
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className={`app-container ${isLoaded ? 'loaded' : ''}`}>
      {/* Animated Background Cursor */}
      <div 
        className="cursor-glow" 
        style={{
          left: `${mousePosition.x}px`,
          top: `${mousePosition.y}px`,
          transform: 'translate(-50%, -50%)'
        }}
      />

      <TestMentorAPI />
      <Navbar scrollY={scrollY} />
      <main>
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-particles">
            {[...Array(20)].map((_, i) => (
              <div 
                key={i} 
                className="particle"
                style={{
                  left: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 5}s`,
                  animationDuration: `${5 + Math.random() * 10}s`
                }}
              />
            ))}
          </div>
          <div className="hero-inner">
            <div className="hero-badge animate-fade-in">
              <span className="badge-pulse"></span>
              India's First Verified Student Job Portal
            </div>
            <h1 className="animate-slide-up">
              Jobs That Match<br/>
              <span className="cyan text-gradient">Your Year.</span> 
              <span className="purple text-gradient">Your Potential.</span>
            </h1>
            <p className="hero-sub animate-fade-in-delay">
              Verified with Aadhaar + College ID. 
              <span className="highlight">Employers reach you based on your year.</span>
            </p>
            <div className="hero-buttons animate-fade-in-delay-2">
              <button className="btn-primary">
                <span>Get Started</span>
                <div className="btn-glow"></div>
              </button>
              <button className="btn-secondary">
                <span>Learn More</span>
              </button>
            </div>
          </div>
        </section>

        <HowItWorks />
        <Verification />

        <section className="section-pad" id="jobs">
          <div className="container">
            <h2 className="section-title">Opportunities For You</h2>
            <div className="jobs-grid">
              {jobs.map(job => <JobCard key={job.id} job={job} />)}
            </div>
          </div>
        </section>

        <Courses />
        <MentorAvailability />
        <ResumeScorer />
        <DashboardPreview />
      </main>
      
      <footer>
        <div className="footer-logo">CareerBridge</div>
        <p>Built with Django + React • 2026</p>
      </footer>
    </div>
  );
};

export default Home;