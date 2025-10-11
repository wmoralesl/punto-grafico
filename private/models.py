from django.db import models
from django.core.cache import cache
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# Create your models here.
class Configuration(models.Model):
    name = models.CharField(max_length=255, default="Organizacion")
    description = models.TextField(blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(
        upload_to='logos/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp'])]
    )
    banner = models.ImageField(
        upload_to='banners/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp'])]
    )
    favicon = models.ImageField(
        upload_to='favicon/',
        blank=True,
        null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['ico'])]
    )
    def clean(self):
        if self.logo and self.logo.size > 2 * 1024 * 1024:  # 2 MB
            raise ValidationError("El logo no puede superar los 2 MB.")
        if self.banner and self.banner.size > 5 * 1024 * 1024:  # 5 MB
            raise ValidationError("El banner no puede superar los 5 MB.")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"

    @staticmethod
    def get_configuration():
        configuration = cache.get('configuration')
        if not configuration:
            configuration = Configuration.objects.first()
            if configuration:
                cache.set('configuration', configuration, 60 * 60)  # Caché por 1 hora
        return configuration

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set('configuration', self, 60 * 60) 

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)  # Descripción breve de la acción
    model_name = models.CharField(max_length=100, null=True, blank=True)  # Modelo afectado
    object_id = models.CharField(max_length=100, null=True, blank=True)  # ID del objeto afectado
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la acción
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # IP del usuario
    additional_info = models.JSONField(null=True, blank=True)  # Información extra en formato JSON

    def __str__(self):
        return f"[{self.timestamp}] {self.user} realizó: '{self.action}'"
    
    class Meta:
        indexes = [
        models.Index(fields=['user']),
        models.Index(fields=['timestamp']),
    ]