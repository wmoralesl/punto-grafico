from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Configuration

@receiver(post_save, sender=Configuration)
def update_configuration_cache(sender, instance, **kwargs):
    """
    Actualiza la caché cuando se guarda una configuración.
    """
    cache.set('configuration', instance, 60 * 60)  # Actualiza la caché por 1 hora

@receiver(post_delete, sender=Configuration)
def clear_configuration_cache(sender, instance, **kwargs):
    """
    Limpia la caché si se elimina una configuración.
    """
    cache.delete('configuration')
