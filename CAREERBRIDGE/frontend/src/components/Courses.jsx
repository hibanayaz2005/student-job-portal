import React from 'react';

const Courses = () => {
  const courseList = [
    { id: 1, provider: "YouTube • CS50", title: "CS50: Introduction to Computer Science", meta: "📚 12 weeks • 🎯 1st Year", diff: "Beginner", type: "yt" },
    { id: 2, provider: "Coursera • Google", title: "Google Data Analytics Certificate", meta: "📚 6 months • 🎯 2nd–3rd Year", diff: "Intermediate", type: "coursera" },
    { id: 3, provider: "NPTEL • IIT Bombay", title: "Data Structures & Algorithms in Python", meta: "📚 8 weeks • 🎯 2nd Year+", diff: "Intermediate", type: "nptel" }
  ];

  return (
    <section className="section-pad courses-section" id="courses">
      <div className="container">
        <div className="section-label">Free Learning</div>
        <h2 className="section-title">Courses to Build Your Career</h2>
        <p className="section-sub">Curated free resources recommended by your year & goals</p>

        <div className="courses-grid">
          {courseList.map(course => (
            <div key={course.id} className="course-card">
              <div className={`course-thumb ${course.type}`}>
                <span>{course.type === 'yt' ? '▶️' : '🎓'}</span>
                <div className="play-overlay"><div className="play-btn-icon">▶</div></div>
              </div>
              <div className="course-body">
                <div className="course-provider">{course.provider}</div>
                <div className="course-title">{course.title}</div>
                <div className="course-meta">{course.meta}</div>
                <div className="course-footer">
                  <span className={`difficulty diff-${course.diff.toLowerCase()}`}>{course.diff}</span>
                  <span className="cert-badge">🏅 Certificate</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Courses;