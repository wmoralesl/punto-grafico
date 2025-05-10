from .models import UserActionLog

def log_user_action(user, action, model_name=None, object_id=None, ip_address=None, additional_info=None):
    UserActionLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        ip_address=ip_address,
        additional_info=additional_info
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip