from django import forms
from .models import TextoAnalizado
import os

class TextoAnalizadoForm(forms.ModelForm):
    class Meta:
        model = TextoAnalizado
        fields = ['titulo', 'archivo']
