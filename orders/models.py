from django.db import models
from users.models import User
from clients.models import Client

# Create your models here.



class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"


class OrderLine(models.Model):
    order = models.ForeignKey(Order, related_name='lines', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.description} ({self.quantity})"
    
