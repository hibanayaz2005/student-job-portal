import React from 'react';

const HowItWorks = () => {
  const steps = [
    { num: '01', icon: '🎓', title: 'Register & Verify', desc: 'Sign up with college email. Upload Aadhaar + College ID.' },
    { num: '02', icon: '✅', title: 'Get Approved', desc: 'Admin reviews in 24hrs. Or use Aadhaar OTP for instant access.' },
    { num: '03', icon: '💼', title: 'Browse Jobs', desc: 'Jobs are filtered by your year and branch automatically.' },
    { num: '04', icon: '🚀', title: 'Apply & Grow', desc: 'Apply with one click. Use the AI Resume Scorer to stand out.' }
  ];

  return (
    <section className="section-pad" id="how">
      <div className="container">
        <div className="section-label">Process</div>
        <h2 className="section-title">How CareerBridge Works</h2>
        <p className="section-sub">Four simple steps from signup to your first job offer</p>
        <div className="steps">
          {steps.map((step) => (
            <div key={step.num} className="step">
              <div className="step-num">{step.num}</div>
              <div className="step-icon">{step.icon}</div>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;