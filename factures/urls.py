from django.urls import path
from . import views

app_name = 'factures'

urlpatterns = [
    path('liste/', views.liste_factures, name='liste_factures'),
    path('creer/', views.creer_facture, name='creer_facture'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
]