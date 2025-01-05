from django.shortcuts import render, redirect, get_object_or_404
from .models import Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet
from django.forms import inlineformset_factory

def creer_facture(request):
    if request.method == 'POST':
        facture_form = FactureForm(request.POST)
        ligne_formset = LigneFactureFormSet(request.POST)

        if facture_form.is_valid() and ligne_formset.is_valid():
            # Sauvegarder la facture
            facture = facture_form.save()

            # Sauvegarder chaque ligne de facture
            for ligne_form in ligne_formset:
                ligne = ligne_form.save(commit=False)
                ligne.facture = facture

                # Récupérer le prix unitaire automatiquement depuis le modèle Produit/Service
                produit_service = ligne.produit_service
                ligne.prix_unitaire = produit_service.prix_unitaire  # Assurez-vous que ce champ existe dans le modèle
                ligne.save()

            # Recalculer le montant total de la facture
            montant_total = sum([ligne.sous_total() for ligne in facture.lignes.all()])
            facture.montant_total = montant_total
            facture.save()

            # Rediriger vers la liste des factures après le succès
            return redirect('factures:liste_factures')
        else:
            # En cas d'erreurs, les afficher sur la page
            context = {
                'facture_form': facture_form,
                'ligne_formset': ligne_formset,
            }
            print(facture_form.errors)
            print(ligne_formset.errors)
            return render(request, 'factures/creer_facture.html', context)
    else:
        # Initialiser les formulaires
        facture_form = FactureForm()
        ligne_formset = LigneFactureFormSet(queryset=LigneFacture.objects.none())

    # Rendu initial de la page de création de facture
    return render(request, 'factures/creer_facture.html', {
        'facture_form': facture_form,
        'ligne_formset': ligne_formset,
    })


def facture_detail(request, pk):
    facture = Facture.objects.get(pk=pk)
    
    entreprise_logo_url = '/static/images/mon_logo1.png'  # Exemple de logo
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
    factures = Facture.objects.all()  # Récupérer toutes les factures
    return render(request, 'factures/liste_factures.html', {'factures': factures})
