# transactions/forms.py

from django import forms
from .models import Transaction, LigneFacture
from produits_services.models import ProduitOuService
from clients.models import Client

class TransactionForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=True,
        empty_label="Sélectionner un client"
    )
    
    lignes = forms.ModelMultipleChoiceField(
        queryset=LigneFacture.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Lignes de facture"
    )

    class Meta:
        model = Transaction
        fields = ['client', 'lignes', 'date_emission', 'montant_total', 'paye']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['montant_total'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        lignes = cleaned_data.get('lignes', [])
        montant_total = 0

        for ligne in lignes:
            montant_total += ligne.montant

        if not lignes:
            self.add_error('lignes', 'Veuillez sélectionner au moins une ligne de facture.')
        
        cleaned_data['montant_total'] = montant_total
        return cleaned_data
