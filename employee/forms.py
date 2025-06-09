from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name',  'phone', 'ubication','is_working', 'position']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'ubication': forms.Select(attrs={'class': 'form-control'}),
            'is_working': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre',
            'phone': 'Teléfono',
            'ubication': 'Ubicación',
            'is_working': 'Activo',
            'position': 'Área de trabajo',

        }