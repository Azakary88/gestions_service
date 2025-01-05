from django import forms
from .models import Facture, LigneFacture
from django.forms import inlineformset_factory

class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['produit_service', 'quantite']

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client']

# Formset pour les lignes de facture
LigneFactureFormSet = inlineformset_factory(
    Facture,
    LigneFacture,
    fields=['produit_service', 'quantite'],
    extra=1,  # Nombre de lignes supplémentaires
    can_delete=True  # Permettre la suppression des lignes
)
