# transactions/admin.py
from django.contrib import admin
from .models import LigneFacture, Facture, ProduitOuService, Transaction

admin.site.register(LigneFacture)
admin.site.register(Facture)
admin.site.register(ProduitOuService)
admin.site.register(Transaction)

