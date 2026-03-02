from django.db import models

class ResumeAnalysis(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.SET_NULL, null=True, blank=True)
    resume_file = models.FileField(upload_to='resume_analyses/')
    overall_score = models.IntegerField()
    section_scores = models.JSONField()  # Breakdown of scores
    improvements = models.JSONField(default=list)
    ats_friendly = models.BooleanField(default=False)
    analyzed_at = models.DateTimeField(auto_now_add=True)