from django.shortcuts import render, redirect
from .forms import ProduitOuServiceForm
from .models import ProduitOuService

# Ajouter un produit ou un service
def ajouter_produit_ou_service(request):
    if request.method == 'POST':
        form = ProduitOuServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits_services')  # Redirige vers la liste des produits/services
    else:
        form = ProduitOuServiceForm()
    return render(request, 'produits_services/ajouter_produit_ou_service.html', {'form': form})

# Lister les produits et services
def liste_produits_services(request):
    produits_services = ProduitOuService.objects.all()
    return render(request, 'produits_services/liste_produits_services.html', {'produits_services': produits_services})
