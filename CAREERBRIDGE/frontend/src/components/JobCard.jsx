import React from 'react';

const JobCard = ({ job }) => {
  return (
    <div className="job-card">
      <div className="job-card-top">
        <div className="company-logo">{job.logo || '🏢'}</div>
        <div>
          <div className="job-title">{job.title}</div>
          <div className="company-name">{job.company} • {job.location}</div>
        </div>
      </div>
      <div className="job-tags">
        <span className="tag tag-type">{job.type}</span>
        <span className="tag tag-year">{job.eligible_years}</span>
        {job.is_new && <span className="tag tag-new">🟢 New</span>}
      </div>
      <div style={{ fontSize: '13px', color: '#6b7a99', marginBottom: '16px', lineHeight: '1.5' }}>
        {job.description}
      </div>
      <div className="job-footer">
        <div className="job-salary">{job.salary}</div>
        <button className="apply-btn">Apply Now</button>
      </div>
    </div>
  );
};

export default JobCard;