from django.db import models
from clients.models import Client
from produits_services.models import ProduitOuService

class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures")
    date_emission = models.DateField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Facture {self.id} - Client: {self.client.nom} - Total: {self.montant_total}"

class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="lignes")
    produit_service = models.ForeignKey(ProduitOuService, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"Ligne - {self.produit_service.nom} (x{self.quantite})"
