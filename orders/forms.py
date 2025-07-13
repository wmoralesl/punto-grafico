# forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderLine

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client']

OrderLineFormSet = inlineformset_factory(Order, OrderLine, fields=('description', 'quantity', 'unit_price'), extra=1)



class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'request_date', 'deadline', 'anticipo',  'responsible', 'current_status']

        labels = {
            'client': 'Cliente',
            'request_date': 'Fecha de Solicitud',
            'deadline': 'Fecha de Entrega',
            'anticipo': 'Anticipo',
            'responsible': 'Responsable',
            'current_status': 'Estado Actual',
        }

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = [ 'quantity', 'description', 'unit_price']
        widgets = {
            'description' : forms.TextInput(attrs={'class': 'form-control', 'rows': 2}),
            'quantity' : forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price' : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Descripción',
            'quantity': 'Cantidad',
            'unit_price': 'Precio Unitario',
        }


        