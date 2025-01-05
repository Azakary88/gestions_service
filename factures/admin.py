from django.contrib import admin
from .models import Facture, LigneFacture

# Enregistrement du modèle Facture
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_emission', 'montant_total')
    search_fields = ('client__nom',)  # Vous pouvez remplacer 'nom' par le champ de recherche réel du modèle Client
    list_filter = ('date_emission',)  # Permet de filtrer par date d'émission

# Enregistrement du modèle LigneFacture
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ('facture', 'produit_service', 'quantite', 'prix_unitaire', 'sous_total')
    search_fields = ('produit_service__nom',)  # Rechercher par nom du produit/service

# Enregistrement des modèles avec l'interface admin
admin.site.register(Facture, FactureAdmin)
admin.site.register(LigneFacture, LigneFactureAdmin)
