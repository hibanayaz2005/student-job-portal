import React from 'react';

const DashboardPreview = () => {
  return (
    <section className="section-pad" style={{ background: 'var(--surface)' }} id="dashboard">
      <div className="container">
        <div className="section-label">Student Dashboard</div>
        <h2 className="section-title">Everything in One Place</h2>
        <p className="section-sub">Track your applications and resume score from your personalized dashboard</p>

        <div className="dashboard-preview">
          <div className="dash-header">
            <div className="dash-title">Good morning, Student 👋</div>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <span className="badge-verified">✓ Verified Student</span>
              <div className="user-avatar">S</div>
            </div>
          </div>
          <div className="dash-body">
            <div className="dash-sidebar">
              <div className="dash-nav-item active">🏠 Dashboard</div>
              <div className="dash-nav-item">💼 Jobs</div>
              <div className="dash-nav-item">📋 Applications</div>
              <div className="dash-nav-item">📚 My Courses</div>
            </div>
            <div className="dash-content">
              <div className="dash-cards">
                <div className="dash-card"><div className="dash-card-val" style={{color:'var(--accent)'}}>12</div><div className="dash-card-label">Jobs Applied</div></div>
                <div className="dash-card"><div className="dash-card-val" style={{color:'var(--accent3)'}}>74</div><div className="dash-card-label">Resume Score</div></div>
                <div className="dash-card"><div className="dash-card-val" style={{color:'#a78bfa'}}>3</div><div className="dash-card-label">Courses Done</div></div>
              </div>
              <div className="recent-apps">
                <h4>Recent Applications</h4>
                <div className="app-row">
                  <div className="app-info"><strong>Zoho Corp</strong><br/><small>Frontend Intern</small></div>
                  <span className="status-badge status-review">Under Review</span>
                </div>
                <div className="app-row">
                  <div className="app-info"><strong>AWS India</strong><br/><small>Cloud Associate</small></div>
                  <span className="status-badge status-applied">Applied</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DashboardPreview;