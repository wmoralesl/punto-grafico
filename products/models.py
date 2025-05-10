from django.db import models
import secrets
def generate_random_id():
    return secrets.token_hex(4)

class TShirt(models.Model):
    # Información básica
    fabric = models.CharField(max_length=100, verbose_name="Tela")
    description = models.TextField(blank=True, verbose_name="Descripción")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de compra")
    stock = models.PositiveIntegerField(verbose_name="Inventario disponible")
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, verbose_name="Talla")

    COLOR_CHOICES = [
        ('white', 'Blanco'),
        ('black', 'Negro'),
        ('red', 'Rojo'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
    ]
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name="Color")

    custom_image = models.ImageField(
        upload_to='tshirts/',
        blank=True,
        null=True,
        verbose_name="Imagen"
    )

    # Información técnica
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f'{self.stock or ""}  {self.fabric or ""} {self.color or ""} {self.size or ""}'.strip()

    class Meta:
        verbose_name = "Playera"
        verbose_name_plural = "Playeras"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre de la etiqueta")

    def __str__(self):
        return self.name
    
class Design(models.Model):
    public = models.CharField(max_length=64, unique=True, default=generate_random_id)
    image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        verbose_name="Diseño"
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de oferta")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tshirts", verbose_name="Categorias")
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    on_offer = models.BooleanField(blank=True, null=True, default=False, verbose_name="En Oferta")


    def __str__(self):
        return f'{self.name} - {self.sale_price}'