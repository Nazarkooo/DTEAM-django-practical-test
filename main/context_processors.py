from django.conf import settings

def settings_context(request):
    """
    Injects Django settings into the template context.
    """
    return {'settings': settings} 