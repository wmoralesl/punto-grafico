from private.models import Configuration

def organization_context(request):
    try:
        config = Configuration.get_configuration  # Obtén configuración general
    except Configuration.DoesNotExist:
        config = None

    return {
        'organization': config
    }

def api_base_url(request):
    from django.conf import settings
    return {"API_BASE_URL": settings.API_BASE_URL}