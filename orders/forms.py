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
        fields = ['client', 'request_date', 'deadline', 'anticipo', 'responsible']

class OrderLineUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['description', 'quantity', 'unit_price']