import React from 'react';

const ResumeScorer = () => {
  const score = 74;

  return (
    <section className="section-pad resume-section" id="resume">
      <div className="container">
        <div className="section-label">AI-Powered</div>
        <h2 className="section-title">Resume Scorer & Analyzer</h2>
        <p className="section-sub">Upload your PDF resume and get an instant score and ATS compatibility check</p>

        <div className="resume-demo">
          <div className="resume-upload-area">
            <div className="upload-big-icon">📄</div>
            <div className="upload-title">Drop your Resume PDF here</div>
            <button className="btn-primary">Upload Resume</button>
          </div>

          <div style={{ borderTop: '1px solid var(--border)', paddingTop: '32px' }}>
            {/* Circular Score Display */}
            <div className="score-display">
              <div className="score-circle" style={{ 
                background: `conic-gradient(var(--accent) 0deg, var(--accent) ${score * 3.6}deg, var(--border) ${score * 3.6}deg)` 
              }}>
                <div className="score-num">{score}</div>
              </div>
              <div className="score-label">Good — A few key improvements could get you to 90+</div>
            </div>

            <div className="score-breakdown">
              <ScoreItem name="Contact Info" val="10/10" percent={100} type="high" feedback="✓ Email, phone, LinkedIn, GitHub all present" />
              <ScoreItem name="Skills Section" val="12/20" percent={60} type="med" feedback="Add 4–6 more technical skills for target roles" />
              <ScoreItem name="Work Experience" val="9/15" percent={60} type="med" feedback="Use strong action verbs & quantify results" />
              <ScoreItem name="Summary" val="6/15" percent={40} type="low" feedback="Too generic — tailor it to your target role" />
            </div>

            <div className="improvements">
              <h4>🚀 Top Improvements</h4>
              <div className="improvement-item">Quantify achievements — e.g., "Built an API serving 10K daily requests"</div>
              <div className="improvement-item">Replace weak verbs like "worked on" with "engineered" or "optimized"</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const ScoreItem = ({ name, val, percent, type, feedback }) => (
  <div className="score-item">
    <div className="score-item-top"><span className="score-item-name">{name}</span><span className="score-item-val">{val}</span></div>
    <div className="progress-bar"><div className={`progress-fill fill-${type}`} style={{ width: `${percent}%` }}></div></div>
    <div className="score-feedback">{feedback}</div>
  </div>
);

export default ResumeScorer;
