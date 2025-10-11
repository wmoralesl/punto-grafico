from django import forms
from .models import Configuration
from users.models import User
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.password_validation import validate_password

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['name', 'logo', 'direction', 'phone', 'email', 'description', 'banner', 'favicon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'direction': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'favicon' : forms.ClearableFileInput(attrs={'class' : 'form-control'}),
        }
        labels = {
            'name': 'Nombre de la Organización',
            'logo': 'Logotipo',
            'direction': 'Dirección',
            'phone': 'Teléfono',
            'email': 'Correo Electrónico',
            'description': 'Descripción Detallada',
            'banner': 'Banner',
            'favicon' : 'Icono de la pagina'
        }

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'second_last_name', 'phone_number', 'date_of_birth', 'gender', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
                ),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombres',
            'last_name': 'Primer apellido',
            'second_last_name': 'Segundo Apellido',
            'phone_number': 'Número de Teléfono',
            'date_of_birth': 'Fecha de Nacimiento',
            'gender': 'Genero',
            'photo': 'Foto de Perfil',
        }


class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Repetir nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, user=None, **kwargs):
        """
        Permite inicializar el formulario con el usuario actual.
        """
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Validar la seguridad de la contraseña
        validate_password(password1, user=self.user)

        return cleaned_data

    def save(self, commit=True):
        """
        Guarda la nueva contraseña para el usuario.
        """
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()