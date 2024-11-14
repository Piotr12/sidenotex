from django import forms
from .models import Sidenote

class SidenoteForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 
            'style': 'width: 100%; box-sizing: border-box;'})
    )
    
    class Meta:
        model = Sidenote
        fields = ['url', 'text']