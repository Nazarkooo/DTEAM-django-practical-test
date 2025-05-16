from django.views.generic import ListView
from .models import LogModel    


class RequestLogListView(ListView):
    model = LogModel
    template_name = 'audit/request_logs.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return LogModel.objects.select_related('user')[:10]
