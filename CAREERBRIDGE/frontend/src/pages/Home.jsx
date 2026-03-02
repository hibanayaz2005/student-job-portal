import React from 'react';
import JobCard from '../components/JobCard';
import Verification from '../components/Verification';
import Courses from '../components/Courses';

const Home = () => {
  const jobs = [
    { id: 1, title: "Frontend Developer Intern", company: "Zoho Corporation", location: "Chennai", type: "Internship", eligible_years: "3rd & Final Year", description: "React, JavaScript, CSS. Work on real products.", salary: "₹15K–20K/mo", is_new: true },
    { id: 2, title: "Cloud Support Associate", company: "AWS India", location: "Remote", type: "Full-time", eligible_years: "Final Year Only", description: "Entry-level cloud role. AWS training provided.", salary: "₹6–8 LPA", is_new: false }
  ];

  return (
    <main>
        <Verification />
        <Courses />
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-badge">India's First Verified Student Job Portal</div>
          <h1>Jobs That Match<br/>
            <span className="cyan">Your Year.</span> <span className="purple">Your Potential.</span>
          </h1>
          <p className="hero-sub">Verified with Aadhaar + College ID. Employers reach you based on your college year, branch, and skills.</p>
          <div className="hero-btns">
            <button className="btn-primary">Start as Student</button>
            <button className="btn-secondary">Post a Job</button>
          </div>
        </div>
      </section>

      <section className="section-pad" id="jobs">
        <div className="container">
          <h2 className="section-title">Opportunities For You</h2>
          <div className="jobs-grid">
            {jobs.map(job => <JobCard key={job.id} job={job} />)}
          </div>
        </div>
      </section>
    </main>
  );
};

export default Home;