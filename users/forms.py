from django import forms
from .models import User  

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'ubication', 'phone_number', 'date_of_birth', 'gender', 'photo', 'role']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d' 
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date_of_birth:
            self.initial['date_of_birth'] = self.instance.date_of_birth.strftime('%Y-%m-%d')