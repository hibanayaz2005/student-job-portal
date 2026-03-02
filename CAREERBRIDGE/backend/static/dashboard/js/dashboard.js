document.addEventListener('DOMContentLoaded', () => {
  function palette(n) {
    const base = [
      '#06b6d4','#7c3aed','#10b981','#f59e0b','#ef4444','#60a5fa','#a78bfa','#34d399','#f97316'
    ];
    const colors = [];
    for (let i = 0; i < n; i++) colors.push(base[i % base.length]);
    return colors;
  }

  function initChart(canvasId, type = 'doughnut') {
    const el = document.getElementById(canvasId);
    if (!el) return;
    const labelsAttr = el.dataset.labels;
    const valuesAttr = el.dataset.values;
    try {
      const labels = JSON.parse(labelsAttr || '[]');
      const values = JSON.parse(valuesAttr || '[]');
      const ctx = el.getContext('2d');
      const colors = palette(labels.length);
      // eslint-disable-next-line no-undef
      if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded');
        return;
      }
      new Chart(ctx, {
        type,
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: colors,
            hoverOffset: 6,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    } catch (err) {
      console.error('Failed to initialize chart', err);
    }
  }

  initChart('rolesChart', 'doughnut');
  initChart('jobsChart', 'doughnut');

  // Load jobs from API and render into the jobs grid
  async function loadJobs() {
    try {
      const resp = await fetch('/api/jobs/');
      const jobs = await resp.json();
      const grid = document.querySelector('.jobs-grid');
      if (!grid) return;
      grid.innerHTML = jobs.map(job => `
        <div class="job-card" data-job-id="${job.id}">
          <div class="job-card-top">
            <div class="company-logo">🏢</div>
            <div>
              <div class="job-title">${job.title}</div>
              <div class="company-name">${job.location}</div>
            </div>
          </div>
          <div class="job-tags">
            <span class="tag tag-type">${job.job_type}</span>
            <span class="tag tag-year">${(job.eligible_years || []).join(', ') || 'All Years'}</span>
          </div>
          <div style="font-size:13px;color:var(--muted);margin-bottom:16px;line-height:1.5;">${(job.description || '').slice(0,160)}</div>
          <div class="job-footer">
            <div class="job-salary">${job.location}</div>
            <button class="apply-btn" ${!job.id ? 'disabled' : ''}>${job.id ? 'Apply Now' : 'Info'}</button>
          </div>
        </div>
      `).join('');

      // attach handlers
      grid.querySelectorAll('.apply-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          const card = btn.closest('.job-card');
          const jobId = card && card.dataset.jobId;
          if (!jobId) return;
          const csrftoken = getCookie('csrftoken');
          try {
            const res = await fetch('/api/jobs/apply/', {
              method: 'POST',
              credentials: 'same-origin',
              headers: Object.assign({'Content-Type':'application/json'}, csrftoken ? {'X-CSRFToken': csrftoken} : {}),
              body: JSON.stringify({ job_id: jobId })
            });
            if (res.status === 201) {
              alert('Applied successfully');
              btn.disabled = true;
              btn.textContent = 'Applied';
            } else if (res.status === 403) {
              const data = await res.json().catch(()=>({}));
              if (data.detail && data.detail.toLowerCase().includes('aptitude')) {
                alert('You must complete the aptitude test before applying.');
              } else {
                alert('Please log in as a student to apply');
                window.location.href = '/accounts/login/';
              }
            } else {
              const data = await res.json().catch(() => ({}));
              alert('Failed to apply: ' + (data.detail || res.status));
            }
          } catch (err) {
            console.error(err);
            alert('Failed to apply');
          }
        });
      });
    } catch (err) {
      console.error('Failed to load jobs', err);
    }
  }

  loadJobs();

  // Job modal functions
  function openJobModal(job) {
    const modal = document.getElementById('job-detail-modal');
    if (!modal) return;
    document.getElementById('job-modal-title').textContent = job.title || 'Job';
    const body = document.getElementById('job-modal-body');
    body.innerHTML = `
      <div style="margin-bottom:8px;color:var(--muted);">${job.location || ''} • ${job.job_type || ''}</div>
      <div style="white-space:pre-wrap;">${job.description || ''}</div>
    `;
    modal.style.display = 'flex';
    modal.dataset.jobId = job.id || '';
    document.getElementById('job-modal-status').textContent = '';
    // disable apply if no job id
    const applyBtn = document.getElementById('job-modal-apply');
    if (!job.id) {
      applyBtn.disabled = true; applyBtn.textContent = 'Not available';
    } else { applyBtn.disabled = false; applyBtn.textContent = 'Apply'; }
  }

  function closeJobModal() {
    const modal = document.getElementById('job-detail-modal'); if (!modal) return; modal.style.display = 'none';
  }

  document.getElementById('job-modal-close')?.addEventListener('click', closeJobModal);
  document.getElementById('job-detail-modal')?.addEventListener('click', (e) => { if (e.target.id === 'job-detail-modal') closeJobModal(); });

  // delegate clicks from jobs grid to open modal with details
  document.querySelector('.jobs-grid')?.addEventListener('click', (e) => {
    const card = e.target.closest('.job-card');
    if (!card) return;
    const jobId = card.dataset.jobId;
    // fetch full job if id exists
    if (jobId) {
      fetch('/api/jobs/').then(r => r.json()).then(list => {
        const job = list.find(j => String(j.id) === String(jobId)) || { id: jobId, title: card.querySelector('.job-title')?.textContent, description: card.querySelector('div[style]')?.textContent, location: card.querySelector('.company-name')?.textContent };
        openJobModal(job);
      }).catch(() => {
        openJobModal({ id: jobId, title: card.querySelector('.job-title')?.textContent, description: card.querySelector('div[style]')?.textContent, location: card.querySelector('.company-name')?.textContent });
      });
    } else {
      // sample job
      openJobModal({ id: null, title: card.querySelector('.job-title')?.textContent, description: card.querySelector('div[style]')?.textContent, location: card.querySelector('.company-name')?.textContent });
    }
  });

  // apply from modal
  document.getElementById('job-modal-apply')?.addEventListener('click', async () => {
    const modal = document.getElementById('job-detail-modal'); if (!modal) return;
    const jobId = modal.dataset.jobId; if (!jobId) return;
    const statusEl = document.getElementById('job-modal-status');
    const csrftoken = getCookie('csrftoken');
    try {
      const res = await fetch('/api/jobs/apply/', { method: 'POST', credentials: 'same-origin', headers: Object.assign({'Content-Type':'application/json'}, csrftoken ? {'X-CSRFToken': csrftoken} : {}), body: JSON.stringify({ job_id: jobId }) });
      if (res.status === 201) { statusEl.textContent = 'Applied successfully'; }
      else if (res.status === 403) { 
        const d = await res.json().catch(()=>({}));
        if (d.detail && d.detail.toLowerCase().includes('aptitude')) {
          statusEl.textContent = 'Complete aptitude test before applying';
        } else {
          statusEl.textContent = 'Please log in as a student to apply';
        }
      }
      else { const d = await res.json().catch(()=>({})); statusEl.textContent = 'Failed: ' + (d.detail || res.status); }
    } catch (err) { statusEl.textContent = 'Request failed'; }
  });

  // Quick tests UI
  function showQuickOutput(msg) {
    const out = document.getElementById('quick-test-output');
    const text = (typeof msg === 'object') ? JSON.stringify(msg, null, 2) : String(msg);
    if (out) out.textContent = text;
  }

  document.getElementById('test-open-jobs')?.addEventListener('click', () => {
    const el = document.getElementById('jobs');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showQuickOutput('Opened Jobs section');
  });

  document.getElementById('test-open-courses')?.addEventListener('click', () => {
    const el = document.getElementById('courses');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showQuickOutput('Opened Courses section');
  });

  document.getElementById('test-me')?.addEventListener('click', async () => {
    try {
      const r = await fetch('/api/auth/me/', { credentials: 'same-origin' });
      const data = await r.json().catch(() => ({}));
      showQuickOutput(r.ok ? data : ('Error: ' + (data.detail || r.status)));
    } catch (err) {
      showQuickOutput('Request failed: ' + err.message);
    }
  });

  document.getElementById('test-jobs-api')?.addEventListener('click', async () => {
    try {
      const r = await fetch('/api/jobs/');
      const data = await r.json().catch(() => ({}));
      showQuickOutput(r.ok ? data : ('Error: ' + (data.detail || r.status)));
    } catch (err) {
      showQuickOutput('Request failed: ' + err.message);
    }
  });
  
  // Upload handlers
  function postFile(url, formData) {
    // include CSRF token for session-authenticated endpoints
    const csrftoken = getCookie('csrftoken');
    return fetch(url, {
      method: 'POST',
      headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
      body: formData,
      credentials: 'same-origin'
    }).then(r => r.json());
  }

  // utility to read cookie
  function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }

  // Resume upload button handler (renders compact score-only result)
  const uploadBtn = document.querySelector('.resume-upload-area .btn-primary');
  function renderResumeScore(data) {
    const container = document.querySelector('.analysis-result');
    if (!container) return;
    const score = data && data.score ? data.score : 0;
    const improvements = (data && data.improvements) ? data.improvements : [];
    const remove = (data && data.remove) ? data.remove : [];
    const sections = (data && data.sections) ? data.sections : {};

    // helper to compute max for each key used when scoring
    const maxFor = (k) => {
      if (k === 'skills') return 20;
      if (k === 'experience') return 15;
      if (k === 'projects') return 20;
      if (k === 'contact_info') return 10;
      if (k === 'education') return 10;
      return 25; // formatting or others
    };

    const sectionHtml = Object.keys(sections).length ? Object.entries(sections).map(([k,v]) => {
      const labelMap = {
        contact_info: 'Contact Info', education: 'Education', skills: 'Skills', experience: 'Work Experience', projects: 'Projects', formatting: 'Formatting'
      };
      const label = labelMap[k] || k.replace('_',' ');
      const max = maxFor(k);
      const pct = Math.round((v / max) * 100);
      const width = Math.min(100, Math.max(0, pct));
      return `
        <div class="score-item" style="margin-bottom:10px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><div style="font-weight:700">${label}</div><div style="font-weight:700;color:var(--accent);">${v}/${max}</div></div>
          <div class="progress-bar" style="height:8px;background:var(--border);border-radius:6px;overflow:hidden;"><div style="width:${width}%;height:100%;background:var(--accent3);"></div></div>
        </div>
      `;
    }).join('') : '';

    container.innerHTML = `
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="font-family:var(--font-head);font-size:18px;font-weight:700;">Analysis Result</div>
        <div style="font-size:13px;color:var(--muted);">• Uploaded Resume</div>
      </div>
      <div style="display:flex;gap:24px;align-items:flex-start;margin-bottom:16px;flex-wrap:wrap;">
        <div class="score-display" style="flex:0 0 180px;text-align:center;">
          <div class="score-circle" style="width:140px;height:140px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 8px;">
            <div class="score-num" style="font-family:var(--font-head);font-size:36px;font-weight:800;color:var(--accent);">${parseInt(score,10) || 0}</div>
          </div>
          <div class="score-label" style="color:var(--muted);">Score</div>
        </div>
        <div style="flex:1 1 360px;">
          ${sectionHtml}
        </div>
      </div>
      <div style="margin-top:6px;">
        <div style="font-weight:700;margin-bottom:8px;color:var(--accent);">Suggested Improvements</div>
        <ul style="margin:0 0 12px 18px;color:var(--muted);">
          ${improvements.length ? improvements.map(i => `<li>${i}</li>`).join('') : '<li>No suggestions — great job!</li>'}
        </ul>
        ${remove.length ? `<div style="font-weight:700;margin-bottom:6px;color:var(--accent);">Remove These (Privacy / Unnecessary)</div><ul style="margin:0 0 0 18px;color:var(--muted);">${remove.map(i => `<li>${i}</li>`).join('')}</ul>` : ''}
      </div>
    `;
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  if (uploadBtn) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf,.doc,.docx';

    const uploadArea = document.querySelector('.resume-upload-area');
    let current = { controller: null, uploading: false, filename: '' };

    function ensureStatusEl() {
      let s = uploadArea.querySelector('.upload-status');
      if (!s) {
        s = document.createElement('div');
        s.className = 'upload-status';
        s.style.marginTop = '12px';
        s.style.display = 'flex';
        s.style.gap = '8px';
        s.style.alignItems = 'center';
        uploadArea.appendChild(s);
      }
      return s;
    }

    function setStatus(text, extraNodes) {
      const s = ensureStatusEl();
      s.innerHTML = '';
      const t = document.createElement('div');
      t.style.color = 'var(--muted)';
      t.style.fontSize = '13px';
      t.textContent = text;
      s.appendChild(t);
      if (Array.isArray(extraNodes)) extraNodes.forEach(n => s.appendChild(n));
    }

    function resetStatus() {
      const s = uploadArea.querySelector('.upload-status');
      if (s) s.remove();
      current.controller = null; current.uploading = false; current.filename = '';
      fileInput.value = '';
    }

    uploadBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
      const f = fileInput.files[0];
      if (!f) return;
      // prepare UI and abort controller
      const controller = new AbortController();
      current.controller = controller; current.uploading = true; current.filename = f.name;

      const cancelBtn = document.createElement('button');
      cancelBtn.className = 'btn-secondary';
      cancelBtn.textContent = 'Cancel Upload';
      cancelBtn.addEventListener('click', () => {
        if (current.controller) current.controller.abort();
        setStatus('Upload cancelled');
        current.uploading = false;
        fileInput.value = '';
      });

      setStatus('Uploading ' + f.name + '...', [cancelBtn]);

      const fd = new FormData();
      fd.append('resume', f);

      // Use fetch directly here so we can abort
      const csrftoken = getCookie('csrftoken');
      fetch('/api/resume/upload/', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
        headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
        signal: controller.signal,
      }).then(async (res) => {
        current.uploading = false;
        if (res.ok) {
            const data = await res.json().catch(() => ({}));
            renderResumeScore(data || {});
            // update upload area title to show filename
            try {
              const titleEl = uploadArea.querySelector('.upload-title');
              if (titleEl) titleEl.textContent = f.name;
              const small = uploadArea.querySelector('.upload-text');
              if (small) {
                small.innerHTML = `<span style="font-size:12px;color:var(--muted);">${(f.size/1024).toFixed(0)} KB — ${f.type || 'file'}</span>`;
              }
              uploadArea.classList.add('uploaded');
            } catch (e) { /* ignore */ }
          // show uploaded state with reupload/cancel option
          const reBtn = document.createElement('button');
          reBtn.className = 'btn-secondary'; reBtn.textContent = 'Re-upload';
          reBtn.addEventListener('click', () => { resetStatus(); fileInput.click(); });

          const removeBtn = document.createElement('button');
          removeBtn.className = 'btn-secondary'; removeBtn.textContent = 'Remove';
          removeBtn.addEventListener('click', () => { resetStatus(); document.querySelector('.analysis-result') && (document.querySelector('.analysis-result').innerHTML = ''); });

          setStatus('Uploaded: ' + f.name, [reBtn, removeBtn]);
        } else {
          const d = await res.json().catch(() => ({}));
          setStatus('Upload failed: ' + (d.detail || res.status));
          fileInput.value = '';
        }
      }).catch(err => {
        if (err.name === 'AbortError') {
          setStatus('Upload aborted');
        } else {
          console.error(err);
          setStatus('Upload failed');
        }
        current.uploading = false; fileInput.value = '';
      });
    });
  }

  // ensure reset also restores upload area title
  function restoreUploadAreaDefault() {
    const uploadArea = document.querySelector('.resume-upload-area');
    if (!uploadArea) return;
    const titleEl = uploadArea.querySelector('.upload-title');
    if (titleEl) titleEl.textContent = 'Drop your Resume PDF here';
    const small = uploadArea.querySelector('.upload-text');
    if (small) small.innerHTML = 'Our AI will analyze it and give you a score out of 100 with detailed feedback';
    uploadArea.classList.remove('uploaded');
  }

  // Verification upload zones: support multiple zones and doc types (uses data-doc-type)
  const uploadZones = document.querySelectorAll('.upload-zone');
  uploadZones.forEach(zone => {
    const docType = zone.dataset.docType || 'aadhaar';
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.png,.jpg,.jpeg';
    zone.addEventListener('click', () => input.click());
    input.addEventListener('change', () => {
      const f = input.files[0];
      if (!f) return;
      const fd = new FormData();
      fd.append('document', f);
      fd.append('doc_type', docType);
      postFile('/api/verify/submit/', fd).then(data => {
        alert('Document uploaded for verification');
        window.location.reload();
      }).catch(err => { console.error(err); alert('Upload failed'); });
    });
  });

  // Sidebar navigation: scroll to section based on data-target
  document.querySelectorAll('.dash-nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const tgt = item.dataset.target;
      if (!tgt) return;
      // toggle active class
      const parent = item.closest('.dash-sidebar');
      if (parent) parent.querySelectorAll('.dash-nav-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      const el = document.getElementById(tgt);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // Course play: only allow play for authenticated users
  document.querySelectorAll('.course-card').forEach(card => {
    const play = card.querySelector('.play-overlay');
    if (!play) return;
    play.style.cursor = 'pointer';
    play.addEventListener('click', async (e) => {
      e.stopPropagation();
      const url = card.dataset.playUrl;
      if (!url) return;
      // check auth
      try {
        const resp = await fetch('/api/auth/me/', { credentials: 'same-origin' });
        if (resp.status === 200) {
          window.open(url, '_blank');
        } else {
          alert('Please log in to access this course');
          window.location.href = '/accounts/login/';
        }
      } catch (err) {
        console.error('Auth check failed', err);
        alert('Please log in to access this course');
        window.location.href = '/accounts/login/';
      }
    });
  });

  // Employer quick-post: prompt-based job post (uses /api/jobs/post/)
  const postBtn = document.querySelector('.hero .btn-secondary');
  if (postBtn) {
    postBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      // gather basic fields via prompts
      const title = prompt('Job title');
      if (!title) return;
      const description = prompt('Short description');
      const job_type = prompt('Job type (internship/full_time)', 'internship');
      const years = prompt('Eligible years (comma separated numbers)', '3,4');
      const location = prompt('Location', 'Remote');
      const deadline = prompt('Deadline (YYYY-MM-DD)', '2026-12-31');

      const payload = {
        title,
        description,
        job_type,
        eligible_years: years.split(',').map(s => parseInt(s.trim())).filter(Boolean),
        location,
        deadline,
      };

      try {
        const csrftoken = getCookie('csrftoken');
        const resp = await fetch('/api/jobs/post/', {
          method: 'POST',
          headers: Object.assign({'Content-Type': 'application/json'}, csrftoken ? {'X-CSRFToken': csrftoken} : {}),
          credentials: 'same-origin',
          body: JSON.stringify(payload),
        });
        if (resp.status === 201) {
          alert('Job posted successfully');
        } else if (resp.status === 403) {
          alert('Only employers may post jobs. Please log in as an employer.');
        } else {
          const data = await resp.json().catch(() => ({}));
          alert('Failed to post job: ' + (data.detail || resp.status));
        }
      } catch (err) {
        console.error(err);
        alert('Failed to post job');
      }
    });
  }
});
