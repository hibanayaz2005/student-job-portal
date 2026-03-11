from reportlab.pdfgen import canvas
from django.conf import settings
import os

def generate_certificate(student_name, test_title, certificate_id):
    
    file_name = f"certificate_{certificate_id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 750, "Certificate of Achievement")

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 650, "This certifies that")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 600, student_name)

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 550, "has successfully passed")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 500, test_title)

    c.setFont("Helvetica", 12)
    c.drawString(50, 100, f"Certificate ID: {certificate_id}")

    c.save()

    return file_name