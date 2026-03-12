# student-job-portal
# CareerBridge (backend)

Quick setup:

1. Create and activate a Python virtualenv and install dependencies.  On **Windows (PowerShell)**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
cd backend           # switch into the backend directory first
pip install -r requirements.txt
```

On **macOS / Linux (bash or zsh)**:

```bash
python3 -m venv .venv
source .venv/bin/activate
cd backend
pip install -r requirements.txt
```

2. Run migrations and start server (already in `backend`):

```powershell
# if there are new model changes, create migrations first
c:\Users\HIBA\OneDrive\Pictures\Screenshots\Screenshot 2026-03-02 062009.pngcdtions
python manage.py migrate
python manage.py runserver
```

The dashboard will be available at `http://127.0.0.1:8000/`.

Once logged in (either via the session login page or using the API tokens), users can complete or update their profile by visiting `http://127.0.0.1:8000/accounts/settings/`.  The settings page is role‑aware and will show the appropriate fields for students or employers, along with a simple completeness indicator.  The login page now offers a **Google sign‑in** button and no longer shows the API hint text – developers should access the API directly at `/api/auth/login/` if needed.

Students can now add a list of **certifications** and a **LinkedIn URL** to their profile; these are stored as comma-separated values in the form.  Additionally, an **aptitude test flag** tracks whether the student has passed a pre‑employment quiz – applications to jobs will be blocked until the flag is true.  (The test itself is not implemented; the field is checked server‑side.)
