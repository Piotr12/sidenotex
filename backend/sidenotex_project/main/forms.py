from django import forms
from .models import Sidenote

class SidenoteForm(forms.ModelForm):
    class Meta:
        model = Sidenote
        fields = ['url', 'text']