from rest_framework import viewsets
from .models import CVModel
from .serializers import CVSerializer

class CVViewSet(viewsets.ModelViewSet):
    queryset = CVModel.objects.prefetch_related('skills', 'projects', 'contacts')
    serializer_class = CVSerializer