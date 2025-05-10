from django import forms
from .models import Design, Tag

class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['image', 'name', 'description', 'sale_price', 'offer_price', 'tags', 'on_offer']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-2'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': 4}),

            'sale_price': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control mb-2'}),
            'on_offer': forms.CheckboxInput(attrs={'class': 'form-check-input mb-2'}),
        }
        labels = {
            'image': 'Imagen',
            'name': 'Nombre del diseño',
            'description': 'Descripción',
            'sale_price': 'Precio Normal',
            'offer_price': 'Precio de Oferta',
            'tags': 'Etiquetas',
            'on_offer': 'En oferta',
        }
