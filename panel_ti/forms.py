from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import PoliticaSesion, Auditoria

class PoliticaSesionForm(forms.ModelForm):
    limite_sesiones = forms.IntegerField(
        label='Límite de sesiones simultáneas por usuario',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5}),
    )
    tiempo_inactividad = forms.IntegerField(
        label='Tiempo máximo de inactividad (minutos)',
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 20}),
    )
    tiempo_expiracion = forms.IntegerField(
        label='Tiempo de expiración del token (minutos)',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10}),
    )
    tiempo_preservacion = forms.IntegerField(
        label='Tiempo de preservación de sesión (minutos)',
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 20}),
    )

    class Meta:
        model = PoliticaSesion
        fields = ['limite_sesiones', 'tiempo_inactividad', 'tiempo_expiracion', 'tiempo_preservacion']

class AuditoriaForm(forms.ModelForm):
    class Meta:
        model = Auditoria
        fields = ['acciones_modificads', 'valor_anterior', 'valor_nuevo']

        labels = {
            'acciones_modificads': 'Acciones modificadas',
            'valor_anterior': 'Valor anterior',
            'valor_nuevo': 'Valor nuevo',
        }

        widgets = {
            'acciones_modificads': forms.Textarea(attrs={'rows': 3}),
            'valor_anterior': forms.Textarea(attrs={'rows': 3}),
            'valor_nuevo': forms.Textarea(attrs={'rows': 3}),
        }
    
                