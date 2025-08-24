from django.db import models
from users.models import User
from clients.models import Client
from employee.models import Employee

# Create your models here.
class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ('recibido', 'Recibido'),
        ('diseno', 'Diseño'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('anulado', 'Anulado'),
    ]

    code = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Clase del ícono de Bootstrap, por ejemplo: 'bi bi-box-seam'")

    def __str__(self):
        return dict(self.STATUS_CHOICES).get(self.code, self.code).title()

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    request_date = models.DateField()
    deadline = models.DateField()
    anticipo = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    responsible = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"
    
    def saldo(self):
        return self.get_total() - self.anticipo
    
    def get_total(self):
        return sum([line.subtotal() for line in self.lines.all()])
    
    def update_total(self):
        self.total = self.get_total()
        self.save(update_fields=['total'])

    def get_lines(self):
        return " • ".join([str(line) for line in self.lines.all()])


class OrderLine(models.Model):
    order = models.ForeignKey(Order, related_name='lines', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f" {self.quantity} {self.description}"
    
