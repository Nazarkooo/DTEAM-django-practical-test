from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import tempfile
from xhtml2pdf import pisa
from django.http import HttpResponse

@shared_task
def send_cv_pdf(cv_id, email):
    from .models import CVModel
    try:
        cv = CVModel.objects.prefetch_related('skills', 'projects', 'contacts').get(id=cv_id)
        
        html = render_to_string('main/cv_pdf.html', {'cv': cv})
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pisa.CreatePDF(html, dest=pdf_file)
            pdf_path = pdf_file.name
        
        subject = f'CV - {cv.first_name} {cv.last_name}'
        message = f'Please find attached the CV for {cv.first_name} {cv.last_name}'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        with open(pdf_path, 'rb') as f:
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
                attachments=[
                    (f'cv_{cv.id}.pdf', f.read(), 'application/pdf')
                ]
            )
        
        return True
    except Exception as e:
        print(f"Error sending CV: {str(e)}")
        return False
