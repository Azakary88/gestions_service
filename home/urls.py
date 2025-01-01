# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # La vue pour l'URL racine
]
