# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet

def creer_facture(request):
    if request.method == 'POST':
        facture_form = FactureForm(request.POST)
        ligne_formset = LigneFactureFormSet(request.POST)

        if facture_form.is_valid() and ligne_formset.is_valid():
            facture = facture_form.save()

            # 🔴 LIGNE CRITIQUE
            ligne_formset.instance = facture

            lignes = ligne_formset.save(commit=False)

            for ligne in lignes:
                if ligne.produit_service:
                    ligne.prix_unitaire = ligne.produit_service.prix_unitaire
                    ligne.save()

            # Gérer les suppressions
            for obj in ligne_formset.deleted_objects:
                obj.delete()

            # 🔴 Recalcul propre
            montant_total = sum(
                ligne.quantite * ligne.prix_unitaire
                for ligne in facture.lignes.all()
            )

            facture.montant_total = montant_total
            facture.save()

            return redirect('factures:liste_factures')

        else:
            print(facture_form.errors)
            print(ligne_formset.errors)

    else:
        facture_form = FactureForm()
        ligne_formset = LigneFactureFormSet()

    return render(request, 'factures/creer_facture.html', {
        'facture_form': facture_form,
        'ligne_formset': ligne_formset,
    })

def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    
    entreprise_logo_url = '/static/images/mon_logo1.png'
    entreprise_nom = "MAIGA GLOBAL SERVICE"
    entreprise_adresse = "IFU :N°00190411X   RCCM : N° BF OHG 2022A555"
    entreprise_telephone = "Burkina Faso, Ouahigouya, sect 01 Tel : 75 50 67 27/51 43 68 65/71 63 18 81"
    entreprise_email = "maigatech2021@gmail.com"
    entreprise_services = "Programmation informatique, Maintenance informatique, Formations en informatique, Maintenance des climatiseurs, Fournitures et consommables informatique,Création de sites Web, location de véhicules, conservation et vente de produits agricoles"
    responsable_nom = "Absatou WEREM"
    
    return render(request, 'factures/facture_detail.html', {
        'facture': facture,
        'entreprise_logo_url': entreprise_logo_url,
        'entreprise_nom': entreprise_nom,
        'entreprise_adresse': entreprise_adresse,
        'entreprise_telephone': entreprise_telephone,
        'entreprise_email': entreprise_email,
        'entreprise_services': entreprise_services,
        'responsable_nom': responsable_nom,
    })

def liste_factures(request):
    factures = Facture.objects.all()
    return render(request, 'factures/liste_factures.html', {'factures': factures})
