from django.urls import path
from . import views

urlpatterns = [
    path('ajouter_produit_ou_service/', views.ajouter_produit_ou_service, name='ajouter_produit_ou_service'),
    path('liste_produits_services/', views.liste_produits_services, name='liste_produits_services'),
]
