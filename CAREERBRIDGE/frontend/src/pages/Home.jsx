import React from 'react';
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
  const jobs = [
    { id: 1, title: "Frontend Developer Intern", company: "Zoho Corporation", location: "Chennai", type: "Internship", eligible_years: "3rd & Final Year", description: "React, JavaScript, CSS. Work on real products.", salary: "₹15K–20K/mo", is_new: true },
    { id: 2, title: "Cloud Support Associate", company: "AWS India", location: "Remote", type: "Full-time", eligible_years: "Final Year Only", description: "Entry-level cloud role. AWS training provided.", salary: "₹6–8 LPA", is_new: false }
  ];

  return (
    <div className="app-container">
      <TestMentorAPI />
      <Navbar />
      <main>
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-inner">
            <div className="hero-badge">India's First Verified Student Job Portal</div>
            <h1>Jobs That Match<br/><span className="cyan">Your Year.</span> <span className="purple">Your Potential.</span></h1>
            <p className="hero-sub">Verified with Aadhaar + College ID. Employers reach you based on your year.</p>
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