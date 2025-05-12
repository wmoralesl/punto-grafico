from django import forms
from .models import Client

class CLientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone']