# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),  # 🔥 dashboard = accueil
    path('accueil/', views.index, name='index'),  # optionnel
]
