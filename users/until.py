from django.utils.timezone import now

def generate_unique_username(instance):
    """
    Genera un nombre de usuario único basado en el nombre, apellido y año actual.
    """
    base_username = (
        instance.first_name[0].lower() + 
        instance.last_name.lower() + 
        (instance.second_last_name[0].lower() if instance.second_last_name else '') +
        str(now().year)[-2:]
    )
    username = base_username
    counter = 1

    while instance.__class__.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username