from django.urls import path
from . import views 
from .utils import remplir_lignes_facture
from .views import ajouter_transaction, telecharger_facture_pdf, facture_detail, generer_factures_automatiquement

urlpatterns = [
    path('ajouter/', views.ajouter_transaction, name='ajouter_transaction'),
    path('', views.liste_transactions, name='liste_transactions'),
    path('generer_factures/<int:facture_id>/', views.generer_factures, name='generer_factures'),
    path('liste_factures/', views.liste_factures, name='liste_factures'),
    path('remplir_lignes_facture/', remplir_lignes_facture, name='remplir_lignes_facture'),
    path('factures/<int:facture_id>/pdf/', telecharger_facture_pdf, name='telecharger_facture_pdf'),
    path('factures/<int:facture_id>/', facture_detail, name='facture_detail'),
    path('factures/generer/', generer_factures_automatiquement, name='generer_factures_automatiquement'),
]
