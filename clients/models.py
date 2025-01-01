from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, default="default@example.com")
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
