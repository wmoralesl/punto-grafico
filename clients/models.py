from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=256)
    phone = models.PositiveBigIntegerField()