import React from 'react';

const Verification = () => {
  return (
    <section className="section-pad" id="verify" style={{ background: 'var(--surface)' }}>
      <div className="container">
        <div className="section-label">Verification</div>
        <h2 className="section-title">Secure Student Verification</h2>
        <p className="section-sub">Only real, enrolled students access the platform — keeping it safe and trusted for employers</p>
        
        <div className="verify-grid">
          <div>
            {/* Aadhaar Card Section */}
            <div className="verify-card" style={{ marginBottom: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h3>Aadhaar Card</h3>
                <span className="badge-pending">⏳ Pending Review</span>
              </div>
              <p>Upload a clear photo of your Aadhaar card. Your Aadhaar number is hashed and never stored in plain text.</p>
              <div className="upload-zone">
                <div className="upload-icon">🪪</div>
                <div className="upload-text">Drag & drop or <strong>click to upload</strong><br/><span style={{ fontSize: '12px' }}>JPG, PNG, PDF — Max 5MB</span></div>
              </div>
              <div style={{ fontSize: '12px', color: 'var(--muted)', display: 'flex', gap: '6px', alignItems: 'center' }}>
                <span>🔒</span> Your data is encrypted and never shared with employers
              </div>
            </div>

            {/* College ID Section */}
            <div className="verify-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h3>College / School ID</h3>
                <span className="badge-verified">✓ Verified</span>
              </div>
              <p>Upload your current valid student ID card. This confirms your year of study and institution.</p>
              <div className="upload-zone" style={{ borderColor: 'rgba(16,185,129,0.3)', background: 'rgba(16,185,129,0.03)' }}>
                <div className="upload-icon">🏫</div>
                <div className="upload-text" style={{ color: 'var(--accent3)' }}>Document verified ✓<br/><span style={{ fontSize: '12px', color: 'var(--muted)' }}>St. Joseph's Engineering College — 3rd Year CSE</span></div>
              </div>
            </div>
          </div>

          {/* Benefits List */}
          <div>
            <div style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '20px', padding: '32px' }}>
              <h3 style={{ fontFamily: 'var(--font-head)', fontSize: '20px', fontWeight: '700', marginBottom: '24px' }}>Verification Benefits</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <BenefitItem emoji="🛡️" title="Trusted Profile Badge" desc="Employers see a verified badge on your profile — 3x more likely to get a callback" />
                <BenefitItem emoji="🎯" title="Year-Matched Jobs" desc="Only see jobs you're eligible for based on your year and branch" />
                <BenefitItem emoji="⚡" title="Instant via Aadhaar OTP" desc="Skip manual review with UIDAI OTP-based instant verification" />
              </div>
              <div style={{ marginTop: '28px', padding: '16px', background: 'rgba(0,229,255,0.06)', border: '1px solid rgba(0,229,255,0.15)', borderRadius: '12px', fontSize: '13px', color: 'var(--muted)' }}>
                <strong style={{ color: 'var(--accent)' }}>Manual review:</strong> Admin approves within 24hrs<br/>
                <strong style={{ color: 'var(--accent3)' }}>Aadhaar OTP:</strong> Instant verification via UIDAI API
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Helper component for the list items
const BenefitItem = ({ emoji, title, desc }) => (
  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
    <span style={{ fontSize: '24px' }}>{emoji}</span>
    <div>
      <div style={{ fontWeight: '600', fontSize: '14px', marginBottom: '4px' }}>{title}</div>
      <div style={{ fontSize: '13px', color: 'var(--muted)' }}>{desc}</div>
    </div>
  </div>
);

export default Verification;