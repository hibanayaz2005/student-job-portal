import React, { useState } from 'react';

const JobCard = ({ job }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  
  const handleApply = () => {
    alert(`Application for ${job.title} at ${job.company} would be processed here. This will connect to the backend API.`);
  };
  
  const handleSave = (e) => {
    e.stopPropagation();
    setIsSaved(!isSaved);
  };
  
  const handleShare = (e) => {
    e.stopPropagation();
    if (navigator.share) {
      navigator.share({
        title: job.title,
        text: `Check out this ${job.type} at ${job.company}`,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Job link copied to clipboard!');
    }
  };

  return (
    <div 
      className={`job-card ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Card Actions */}
      <div className="card-actions">
        <button 
          className={`save-btn ${isSaved ? 'saved' : ''}`}
          onClick={handleSave}
          title={isSaved ? 'Remove from saved' : 'Save job'}
        >
          {isSaved ? '💾' : '🔖'}
        </button>
        <button 
          className="share-btn"
          onClick={handleShare}
          title="Share job"
        >
          📤
        </button>
      </div>
      
      <div className="job-card-top">
        <div className="company-logo">
          {job.logo || '🏢'}
          {job.is_new && <span className="new-badge">NEW</span>}
        </div>
        <div>
          <div className="job-title">{job.title}</div>
          <div className="company-name">
            {job.company} • {job.location}
            <span className="location-icon">📍</span>
          </div>
        </div>
      </div>
      
      <div className="job-tags">
        <span className={`tag tag-type ${job.type.toLowerCase().includes('intern') ? 'internship' : 'fulltime'}`}>
          {job.type}
        </span>
        <span className="tag tag-year">{job.eligible_years}</span>
        <span className="tag tag-salary">{job.salary}</span>
      </div>
      
      <div className="job-description">
        <p>{job.description}</p>
      </div>
      
      <div className="job-footer">
        <button className="apply-btn" onClick={handleApply}>
          <span>Apply Now</span>
          <div className="btn-shine"></div>
        </button>
        <div className="job-meta">
          <span className="posted-time">Posted 2 days ago</span>
          <span className="applicants">23 applicants</span>
        </div>
      </div>
    </div>
  );
};

export default JobCard;