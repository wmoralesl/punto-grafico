from django.db import models
from django.core.exceptions import ValidationError

def validate_eight_digits(value):
    if len(str(value)) != 8:
        raise ValidationError('El valor debe tener exactamente 8 dígitos.')


class Employee(models.Model):
    POSITION_CHOICES = [
        ('atencion', 'Atención al Cliente'),
        ('costura', 'Costura y Confección'),
        ('impresion', 'Impresión'),
        ('sublimacion', 'Sublimación'),
    ]
    UBICATION_CHOICES = (
        ('sl', 'San Luis'),
        ('ip', 'Ipala'),
    )
    name = models.CharField(max_length=60)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    phone = models.IntegerField(
        validators=[validate_eight_digits],
        blank=True, null=True
    )
    is_working = models.BooleanField(default=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='atencion')
    ubication = models.CharField(max_length=20, choices=UBICATION_CHOICES, default='sl')
    # payment_dates = models.ManyToManyField(PaymentDate, related_name='employees_related', blank=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.name

class Payment(models.Model):
    date = models.IntegerField()
    mount = models.IntegerField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)