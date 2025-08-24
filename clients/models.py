from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=256)
    phone = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)    
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name