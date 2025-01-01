# home/views.py
from django.shortcuts import render, get_object_or_404
from transactions.models import Facture

def index(request):
    facture = Facture.objects.first()
    return render(request, 'home/base.html', {'facture': facture})  # Remplacez par le chemin correct de votre template
