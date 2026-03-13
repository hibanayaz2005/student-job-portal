from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ResumeAnalysis

import re
import tempfile
import os

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    import docx
except Exception:
    docx = None


def extract_text(uploaded_file):
    name = (uploaded_file.name or '').lower()
    data = ''
    # write to temp file for libraries that need a filename
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(name)[1] or '.dat') as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        if name.endswith('.pdf') and PdfReader is not None:
            try:
                reader = PdfReader(tmp_path)
                pages = [p.extract_text() or '' for p in reader.pages]
                data = '\n'.join(pages)
            except Exception:
                data = ''
        elif (name.endswith('.docx') or name.endswith('.doc')) and docx is not None:
            try:
                doc = docx.Document(tmp_path)
                data = '\n'.join(p.text for p in doc.paragraphs)
            except Exception:
                data = ''
        else:
            # fallback: try reading raw bytes and decode
            try:
                with open(tmp_path, 'rb') as f:
                    raw = f.read()
                data = raw.decode('utf-8', errors='ignore')
            except Exception:
                data = ''
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    return data or ''


def score_resume_text(text):
    # simple heuristic scoring (0-100) across categories
    text_low = text.lower()

    scores = {}

    # Contact info (0-10)
    email = bool(re.search(r"[\w.+-]+@[\w.-]+\\.[a-zA-Z]{2,}", text))
    phone = bool(re.search(r"\b\d{10}\b", re.sub(r"[^0-9]", '', text))) or bool(re.search(r"\+?\d[\d\s-]{8,}\d", text))
    linkedin = 'linkedin.com' in text_low or 'github.com' in text_low
    scores['contact_info'] = int(min(10, (4 if email else 0) + (3 if phone else 0) + (3 if linkedin else 0)))

    # Education (0-10)
    edu_terms = ['b.tech', 'b.e', 'bsc', 'bachelor', 'm.tech', 'm.sc', 'bca', 'bcom', 'cgpa', 'gpa', 'degree']
    edu_found = any(t in text_low for t in edu_terms)
    scores['education'] = 10 if edu_found else 4

    # Skills (0-20)
    skill_keywords = ['python','java','c++','c#','javascript','react','node','django','flask','sql','git','aws','docker','kubernetes','tensorflow','pytorch','html','css','aws','linux']
    found_skills = sum(1 for k in skill_keywords if k in text_low)
    scores['skills'] = int(min(20, found_skills * 3))

    # Experience (0-15)
    exp_terms = ['intern', 'experience', 'worked', 'project', 'team', 'lead']
    exp_count = sum(text_low.count(t) for t in exp_terms)
    if exp_count >= 6:
        scores['experience'] = 15
    elif exp_count >= 3:
        scores['experience'] = 9
    else:
        scores['experience'] = 4

    # Projects (0-20)
    projects = 'project' in text_low or 'github.com' in text_low
    scores['projects'] = 20 if projects else (10 if 'portfolio' in text_low else 4)

    # ATS friendliness / formatting (0-25)
    # heuristics: presence of bullets, short lines, absence of table markers
    bullets = '•' in text or '- ' in text
    tables = '<table' in text_low or '|' in text_low and text_low.count('\n')>5
    length = len(text_low)
    formatting = 0
    if bullets and not tables:
        formatting = 20
    elif bullets and tables:
        formatting = 10
    else:
        formatting = 8 if length > 400 else 4
    scores['formatting'] = int(min(25, formatting))

    # aggregate to overall score
    overall = scores['contact_info'] + scores['education'] + scores['skills'] + scores['experience'] + scores['projects'] + scores['formatting']
    # normalize if not exactly 100
    overall = int(max(0, min(100, overall)))

    return overall, scores


def detect_unnecessary(text):
    """Return a list of unnecessary personal items to remove from resumes."""
    t = text.lower()
    removes = []

    # Photo
    if 'photo' in t or 'passport size' in t or 'photograph' in t:
        removes.append('Photo (remove unless explicitly required by employer)')

    # DOB / age / marital status / father's name
    if 'date of birth' in t or '\bdob\b' in t:
        removes.append('Date of birth / age')
    if 'marital status' in t or 'marital' in t:
        removes.append('Marital status')
    if "father" in t and 'name' in t:
        removes.append("Father's name / parent details")

    # References
    if 'references' in t or 'reference' in t:
        removes.append('References section (provide on request)')

    # Full permanent address (long addresses)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if any('permanent address' in ln.lower() for ln in lines) or sum(1 for ln in lines if re.search(r'\b\d{6}\b', ln)) > 0:
        # heuristic: long permanent addresses or PIN codes
        removes.append('Full permanent address (keep city/state only)')

    # Gender / nationality
    if '\bgender\b' in t or 'nationality' in t:
        removes.append('Gender / Nationality')

    # Hobbies — only keep if directly relevant
    if 'hobbies' in t or 'interests' in t:
        removes.append('Hobbies/Interests (remove or keep concise and relevant)')

    # Lengthy objective / personal statement
    if any(len(ln) > 200 for ln in lines[:8]):
        removes.append('Long personal objective/summary (make it short and targeted)')

    # Deduplicate
    uniq = []
    for r in removes:
        if r not in uniq:
            uniq.append(r)
    return uniq


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    def post(self, request):
        student = getattr(request.user, 'student_profile', None)
        resume_file = request.FILES.get('resume') or request.FILES.get('document')
        if not resume_file:
            return Response({'detail': 'No file provided'}, status=400)

        text = extract_text(resume_file)
        overall, section_scores = score_resume_text(text)

        improvements = []
        if section_scores.get('skills', 0) < 8:
            improvements.append('Add more technical skills and keywords relevant to target role')
        if section_scores.get('education', 0) < 8:
            improvements.append('Include degree, college and CGPA if relevant')
        if section_scores.get('projects', 0) < 12:
            improvements.append('Add 1–2 projects with problem, approach and results')

        ats_friendly = section_scores.get('formatting', 0) >= 15 and '<table' not in text.lower()

        # detect unnecessary personal data and suggest removals
        remove_items = detect_unnecessary(text)
        for it in remove_items:
            improvements.append('Remove unnecessary data: ' + it)

        analysis = ResumeAnalysis.objects.create(
            student=student,
            resume_file=resume_file,
            overall_score=overall,
            section_scores=section_scores,
            improvements=improvements,
            ats_friendly=False,
            ats_friendly=ats_friendly,
        )

        try:
            if student:
                student.resume_score = analysis.overall_score
                student.save()
        except Exception:
            pass

        return Response({'status': 'analyzed', 'score': analysis.overall_score, 'sections': analysis.section_scores, 'improvements': analysis.improvements, 'remove': remove_items})
