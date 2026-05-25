from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
            'role': 'Rol',
        }

        widgets = {
            'password': forms.PasswordInput(attrs={'min_length': 8}),
            'username': forms.TextInput(attrs={'min_length': 4}),
            'role': forms.Select(choices=User.ROLE)
        }

