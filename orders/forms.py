# forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderLine

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client']

OrderLineFormSet = inlineformset_factory(Order, OrderLine, fields=('description', 'quantity', 'unit_price'), extra=1)



class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'request_date', 'deadline', 'anticipo', 'total', 'responsible']
