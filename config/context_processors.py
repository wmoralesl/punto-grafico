from private.models import Configuration

def organization_context(request):
    try:
        config = Configuration.get_configuration  # Obtén configuración general
    except Configuration.DoesNotExist:
        config = None

    return {
        'organization': config
    }
