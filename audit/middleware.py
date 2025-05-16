from .models import LogModel
from django.db import transaction

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        try:
            with transaction.atomic():
                if not request.path.startswith("/logs/"):
                    LogModel.objects.create(
                        method=request.method,
                        path=request.path,
                        query_string=request.META.get('QUERY_STRING', ''),
                        remote_addr=request.META.get('REMOTE_ADDR'),
                        user=request.user if request.user.is_authenticated else None
                )
        except Exception:
            pass
        
        return response 