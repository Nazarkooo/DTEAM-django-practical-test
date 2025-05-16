from django.views.generic import ListView, DetailView, TemplateView
from .models import CVModel
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .tasks import send_cv_pdf
from .translation import translate_text, SUPPORTED_LANGUAGES


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = SUPPORTED_LANGUAGES
        return context
    
    def post(self, request, *args, **kwargs):
        cv = self.get_object()
        
        if 'email' in request.POST:
            email = request.POST.get('email')
            if email:
                send_cv_pdf.delay(cv.id, email)
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Email is required'})
            
        elif 'translate' in request.POST:
            language = request.POST.get('language')
            if not language:
                return JsonResponse({'status': 'error', 'message': 'Language is required'})

            translated_data = {
                'first_name': translate_text(cv.first_name, language),
                'last_name': translate_text(cv.last_name, language),
                'bio': translate_text(cv.bio, language),
                'skills': [
                    {'id': skill.id, 'skill': translate_text(skill.skill, language)}
                    for skill in cv.skills.all()
                ],
                'projects': [
                    {
                        'id': project.id,
                        'project': translate_text(project.project, language),
                        'description': translate_text(project.description, language)
                    }
                    for project in cv.projects.all()
                ],
                'contacts': [
                    {'id': contact.id, 'type': contact.type, 'contact': contact.contact}
                    for contact in cv.contacts.all()
                ]
            }
            
            return JsonResponse({
                'status': 'success',
                'translated': translated_data
            })


class SettingsView(TemplateView):
    template_name = 'main/settings.html'


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
