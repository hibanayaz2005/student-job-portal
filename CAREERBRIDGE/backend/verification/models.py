from django.db import models

class VerificationDocument(models.Model):
    DOC_TYPE = [('aadhaar', 'Aadhaar Card'), ('college_id', 'College ID Card')]
    STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.SET_NULL, null=True, blank=True)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE)
    document_file = models.FileField(upload_to='verification_docs/')
    
    # Aadhaar security: store hash only, never raw numbers
    aadhaar_hash = models.CharField(max_length=64, blank=True)
    
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass