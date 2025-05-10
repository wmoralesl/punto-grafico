from django import forms
from .models import User  

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'gender', 'photo', 'role']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',  
                'class': 'form-control',  
            }),
        }
