# produits_services/models.py

from django.db import models

class ProduitOuService(models.Model):
    TYPE_CHOICES = (
        ('produit', 'Produit'),
        ('service', 'Service'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=255)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"
