import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import VerificationDocument
from rest_framework.permissions import IsAuthenticated, AllowAny


class UploadVerificationDocView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    def post(self, request):
        student = getattr(request.user, 'student_profile', None)
        doc_type = request.data.get('doc_type')  # 'aadhaar' or 'college_id'
        doc_file = request.FILES.get('document')

        # Hash Aadhaar number if provided (never store raw)
        aadhaar_num = request.data.get('aadhaar_number')
        a_hash = ""
        if doc_type == 'aadhaar' and aadhaar_num:
            a_hash = hashlib.sha256(aadhaar_num.replace(' ', '').encode()).hexdigest()

        # If student is present, try update_or_create; otherwise create a record with null student
        if student:
            doc, created = VerificationDocument.objects.update_or_create(
                student=student,
                doc_type=doc_type,
                defaults={
                    'document_file': doc_file,
                    'status': 'pending',
                    'aadhaar_hash': a_hash
                }
            )
        else:
            doc = VerificationDocument.objects.create(
                student=None,
                doc_type=doc_type,
                document_file=doc_file,
                status='pending',
                aadhaar_hash=a_hash
            )

        return Response({'status': 'uploaded', 'doc_type': doc_type})


# Maintain the old import name expected by urls.py
SubmitVerificationView = UploadVerificationDocView


class VerificationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student_profile
        doc_type = request.query_params.get('doc_type')

        if doc_type:
            try:
                doc = VerificationDocument.objects.get(student=student, doc_type=doc_type)
                return Response({'doc_type': doc.doc_type, 'status': doc.status, 'uploaded_at': doc.uploaded_at})
            except VerificationDocument.DoesNotExist:
                return Response({'detail': 'No document found for that type'}, status=404)

        # If no doc_type provided, return all documents for the student
        docs = VerificationDocument.objects.filter(student=student)
        data = [{'doc_type': d.doc_type, 'status': d.status, 'uploaded_at': d.uploaded_at} for d in docs]
        return Response({'documents': data})