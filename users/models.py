from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from .until import generate_unique_username
from PIL import Image
import secrets

def generate_random_id():
    return secrets.token_hex(32)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('invited', 'Invitado'),
        ('creator', 'Creador'),
        ('admin', 'Administrador'),
    )
    GENDER_CHOICES = (
    ('male', 'Masculino'),
    ('female', 'Femenino'),
    ('prefer_not_to_say', 'Prefiero no decirlo'),
    )

    UBICATION_CHOICES = (
        ('sl', 'San Luis'),
        ('ip', 'Ipala'),
    )
    id = models.CharField(primary_key=True, max_length=64, unique=True, default=generate_random_id)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    second_last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='creator')
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    ubication = models.CharField(max_length=255, choices=UBICATION_CHOICES, default='sl', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)


    USERNAME_FIELD = 'email'  # Usa email como identificador principal
    REQUIRED_FIELDS = ['role', 'username']

    def soft_delete(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        # Generar un username único si no existe
        if not self.username:
            self.username = generate_unique_username(self)
        
        # Llamar al método save del padre para garantizar que la imagen está disponible
        super().save(*args, **kwargs)

        # Procesar la imagen de la foto si está presente
        if self.photo:
            self._resize_image()

        # Asignar permisos específicos según el rol
        self.assign_permissions()

    def _resize_image(self):
        """
        Redimensiona la imagen a un tamaño máximo de 300x300 px si es necesario.
        """
        img_path = self.photo.path
        img = Image.open(img_path)
        max_size = (300, 300)

        if img.height > 300 or img.width > 300:
            img.thumbnail(max_size, Image.LANCZOS)  # Usar Image.LANCZOS directamente
            img.save(img_path)

    def assign_permissions(self):
        """Asigna permisos al usuario según su rol."""
        # Elimina permisos actuales para evitar duplicados
        self.user_permissions.clear()

        # Obtén los permisos según el rol
        if self.role == 'creator':
            permissions = Permission.objects.filter(codename__in=['view_user'])  # Permiso para ver usuarios
        elif self.role == 'admin':
            permissions = Permission.objects.filter(codename__in=['add_user', 'change_user', 'delete_user', 'view_user', 'change_configuration'])  # Permisos de administrador
        else:
            permissions = []

        # Asignar permisos al usuario
        self.user_permissions.add(*permissions)
    
    def get_full_name(self):
        return f'{self.first_name or ""} {self.last_name or ""} {self.second_last_name or ""}'.strip()
    
    def get_MyUser(self):
        MyUser = User.objects.get(email=self.email)
        return MyUser

    def __str__(self):
        return f'{self.get_full_name()} - {self.is_active}'