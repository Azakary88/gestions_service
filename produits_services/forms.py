from django import forms
from .models import ProduitOuService

class ProduitOuServiceForm(forms.ModelForm):
    class Meta:
        model = ProduitOuService
        fields = ['type', 'nom', 'description', 'prix_unitaire']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }
