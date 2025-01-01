from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TransactionForm
from .models import Transaction, Facture, LigneFacture
from io import BytesIO
from reportlab.pdfgen import canvas
from django.db import transaction as db_transaction
from clients.models import Client
from django.urls import path 
from .utils import remplir_lignes_facture
import logging, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

logger = logging.getLogger(__name__)

def ajouter_transaction(request):
    lignes = LigneFacture.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            lignes_ids = request.POST.getlist('lignes')
            transaction.lignes.set(LigneFacture.objects.filter(id__in=lignes_ids))
            form.save_m2m()

            # Créer une facture pour la transaction
            facture = Facture.objects.create(
                client=transaction.client,
                date_emission=transaction.date_emission
            )
            facture.lignes.set(transaction.lignes.all())
            facture.save()

            transaction.facture = facture
            transaction.save()

            return redirect('liste_transactions')
        else:
            print(form.errors)
    else:
        form = TransactionForm()
    return render(request, 'transactions/ajouter_transaction.html', {'form': form, 'lignes': lignes})


def liste_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/liste_transactions.html', {'transactions': transactions})

def liste_factures(request):
    factures = Facture.objects.all()
    return render(request, 'transactions/liste_factures.html', {'factures': factures})


def generer_factures_automatiquement(request):
    try:
        # Identifier les clients ayant des transactions non payées
        clients_transactions = Transaction.objects.filter(paye=False).values('client_id').distinct()

        for client in clients_transactions:
            client_id = client['client_id']
            transactions_non_payees = Transaction.objects.filter(client_id=client_id, paye=False)

            if transactions_non_payees.exists():
                facture = Facture.objects.create(client_id=client_id)
                lignes_facture = [
                    LigneFacture(
                        facture=facture,
                        transaction=trans,
                        produit_service=trans.produit_service,
                        quantite=trans.quantite
                    )
                    for trans in transactions_non_payees
                ]
                LigneFacture.objects.bulk_create(lignes_facture)

                transactions_non_payees.update(paye=True)

        return HttpResponse("Factures générées avec succès !", status=200)
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des factures : {str(e)}", status=500)

def generer_factures(request, facture_id):
    try:
        # Trouver la facture correspondante à l'ID fourni
        facture = Facture.objects.get(id=facture_id)
        
        # Trouver les transactions non payées associées au client de la facture
        transactions_non_payées = Transaction.objects.filter(client_id=facture.client_id, paye=False)

        if transactions_non_payées.exists():
            lignes_facture = [
                LigneFacture(
                    facture=facture,
                    transaction=trans,
                    produit_service=trans.produit_service,
                    quantite=trans.quantite
                )
                for trans in transactions_non_payées
            ]
            LigneFacture.objects.bulk_create(lignes_facture)

            transactions_non_payées.update(paye=True)
            
            return HttpResponse("Facture générée avec succès !", status=200)
        else:
            return HttpResponse("Aucune transaction non payée trouvée.", status=200)
    except Facture.DoesNotExist:
        return HttpResponse("Facture non trouvée.", status=404)
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération de la facture : {str(e)}", status=500)


def telecharger_facture_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    lignes = facture.factures_ligne_set.all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Facture #{facture.id}")
    width, height = A4

    # Titre et informations client
    pdf.drawString(2 * cm, height - 2 * cm, f"Facture ID: {facture.id}")
    pdf.drawString(2 * cm, height - 2.5 * cm, f"Client: {facture.client.nom}")
    pdf.drawString(2 * cm, height - 3 * cm, f"Date d'émission: {facture.date_emission}")

    # En-têtes de table
    pdf.drawString(2 * cm, height - 4 * cm, "Désignation")
    pdf.drawString(10 * cm, height - 4 * cm, "Prix Unitaire")
    pdf.drawString(14 * cm, height - 4 * cm, "Quantité")
    pdf.drawString(18 * cm, height - 4 * cm, "Prix Total")

    y = height - 4.5 * cm
    for ligne in lignes:
        pdf.drawString(2 * cm, y, ligne.produit_service.nom)
        pdf.drawString(10 * cm, y, f"{ligne.produit_service.prix_unitaire}€")
        pdf.drawString(14 * cm, y, f"{ligne.quantite}")
        pdf.drawString(18 * cm, y, f"{ligne.montant}€")
        y -= 0.5 * cm

    # Montant total
    pdf.drawString(2 * cm, y - 1 * cm, f"Montant Total: {facture.montant_total}€")

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=facture_{facture.id}.pdf'
    return response

def facture_detail(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    return render(request, 'transactions/facture_detail.html', {'facture': facture})
