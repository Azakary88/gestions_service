from django.urls import path
from . import views

urlpatterns = [
    path('ajouter/', views.ajouter_client, name='ajouter_client'),
    path('liste/', views.liste_clients, name='liste_clients'),
]
