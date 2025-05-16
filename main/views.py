from django.views.generic import ListView, DetailView
from .models import CVModel
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa


class CVListView(ListView):
    model = CVModel
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'

    def get_queryset(self):
        return CVModel.objects.prefetch_related('skills', 'projects', 'contacts').all()

class CVDetailView(DetailView):
    model = CVModel
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'

    def get_queryset(self):
        return CVModel.objects.prefetch_related('skills', 'projects', 'contacts')

def download_pdf(request, pk):
    cv = get_object_or_404(CVModel.objects.prefetch_related('skills', 'projects', 'contacts'), pk=pk)
    template = get_template('main/cv_pdf.html')
    html = template.render({'cv': cv})
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv.first_name}_{cv.last_name}_CV.pdf"'
        return response
    
    return HttpResponse('Error generating PDF', status=404)
