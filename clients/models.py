from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=256)
    phone = models.PositiveBigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
