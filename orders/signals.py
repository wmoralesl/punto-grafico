from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLine

@receiver(post_save, sender=OrderLine)
@receiver(post_delete, sender=OrderLine)
def update_order_total(sender, instance, **kwargs):
    instance.order.update_total()
