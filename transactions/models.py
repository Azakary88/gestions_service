# transactions/models.py

from django.db import models
from clients.models import Client
from produits_services.models import ProduitOuService
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

class LigneFacture(models.Model):
    facture = models.ForeignKey('Facture', on_delete=models.CASCADE, related_name='lignes_facture')  # Nom explicite pour la relation
    produit_service = models.ForeignKey(ProduitOuService, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    quantite = models.PositiveIntegerField(default=1)
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.montant:
            self.montant = self.produit_service.prix_unitaire * self.quantite
        super().save(*args, **kwargs)

    def __str__(self): 
        return f"{self.produit_service.nom} - {self.quantite} - {self.montant}€"


class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures")
    date_emission = models.DateField(default=now)
    lignes = models.ManyToManyField(LigneFacture, related_name="factures_associees")  # Nom explicite pour éviter les conflits
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ouverte = models.BooleanField(default=False)
    _updating_total = models.BooleanField(default=False, editable=False)

    def mettre_a_jour_montant_total(self):
        if not self._updating_total:
            self._updating_total = True
            self.montant_total = sum(ligne.montant for ligne in self.lignes.all())
            super().save(update_fields=['montant_total'])
            self._updating_total = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.mettre_a_jour_montant_total()

    def __str__(self):
        return f"Facture #{self.id} - {self.client.nom}"

@receiver(post_save, sender=Facture)
def mettre_a_jour_montant_total_facture(sender, instance, **kwargs):
    if not instance._updating_total:
        instance.mettre_a_jour_montant_total()

class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    lignes = models.ManyToManyField(LigneFacture, blank=True)
    date_emission = models.DateField(default=now)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    paye = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction de {self.client.nom}"
