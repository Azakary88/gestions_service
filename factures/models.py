# models.py
from django.db import models
from clients.models import Client
from produits_services.models import ProduitOuService
from datetime import datetime

class Facture(models.Model):

    TYPE_CHOICES = [
        ('facture', 'Facture'),
        ('proforma', 'Facture Proforma'),
        ('livraison', 'Bordereau de Livraison'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures")
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='facture')

    date_emission = models.DateField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    numero_facture = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.numero_facture:
            annee = datetime.now().year

            count = Facture.objects.filter(
                date_emission__year=annee,
                type_document=self.type_document
            ).count() + 1

            prefix = {
                'facture': 'F',
                'proforma': 'PF',
                'livraison': 'BL'
            }

            self.numero_facture = f"{prefix[self.type_document]}-{count:02d}/{annee}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_facture} - {self.client.nom} - {self.montant_total}"
class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="lignes")
    produit_service = models.ForeignKey(ProduitOuService, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.CharField(max_length=255, blank=True)

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"Ligne - {self.produit_service.nom} (x{self.quantite})"

