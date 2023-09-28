from django import forms
from .models import Diagnostico  # Asumiendo que tienes un modelo Diagnostico

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['nombre', 'marca', 'n_serie', 'modelo', 'ubicacion', 'diagnostico', 'solucion', 'estado']
