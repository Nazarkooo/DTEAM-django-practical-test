from django.views.generic import ListView, DetailView
from .models import CVModel

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
    