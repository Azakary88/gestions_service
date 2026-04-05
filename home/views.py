from django.shortcuts import render

from django.shortcuts import render
from factures.models import Facture
from clients.models import Client
from produits_services.models import ProduitOuService
from django.db.models import Sum

def dashboard(request):
    total_factures = Facture.objects.count()
    total_clients = Client.objects.count()
    total_produits = ProduitOuService.objects.count()
    chiffre_affaires = Facture.objects.aggregate(Sum('montant_total'))['montant_total__sum'] or 0

    context = {
        'total_factures': total_factures,
        'total_clients': total_clients,
        'total_produits': total_produits,
        'chiffre_affaires': chiffre_affaires,
    }

    return render(request, 'home/dashboard.html', context)
def index(request):
    return render(request, 'home/index.html')
