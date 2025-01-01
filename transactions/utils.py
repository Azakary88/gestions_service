from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import render_to_string
from django.utils import timezone
from .models import LigneFacture, ProduitOuService
from django.http import HttpResponse
from transactions.models import Facture

def generer_pdf_facture(facture):
    # Créer un flux de données en mémoire
    buffer = BytesIO()

    # Créer le canvas pour le PDF
    p = canvas.Canvas(buffer, pagesize=letter)

    # Ajouter les informations de la facture
    p.setFont("Helvetica", 12)
    
    # En-tête
    p.drawString(100, 750, f"Facture No: {facture.id}")
    p.drawString(100, 735, f"Date d'émission: {facture.date_emission}")
    p.drawString(100, 720, f"Date d'échéance: {facture.date_limite}")
    p.drawString(100, 705, f"Client: {facture.client.nom}")
    p.drawString(100, 690, f"Adresse: {facture.client.adresse}")
    
    # Ligne séparatrice
    p.setStrokeColor(colors.black)
    p.line(50, 675, 550, 675)

    # Détails des produits/services
    y_position = 650
    p.drawString(100, y_position, "Description")
    p.drawString(400, y_position, "Prix (€)")

    y_position -= 20

    for produit in facture.produits.all():
        p.drawString(100, y_position, produit.nom)
        p.drawString(400, y_position, f"{produit.prix}€")
        y_position -= 20
    
    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, f"Total: {facture.montant_total}€")

    # Finaliser le PDF
    p.showPage()
    p.save()

    # Revenir au début du flux pour récupérer le PDF généré
    buffer.seek(0)
    return buffer

def creer_lignes_facture(facture_id):
    try:
        # Récupération de la facture correspondante
        facture = Facture.objects.get(id=facture_id)
    except Facture.DoesNotExist:
        raise ValueError(f"Facture avec l'ID {facture_id} n'existe pas.")

    # Récupération de tous les produits ou services
    produits = ProduitOuService.objects.all()

    # Création des lignes de facture
    for produit in produits:
        ligne = LigneFacture(
            facture=facture,  # Lien avec la facture
            produit_service=produit,
            description=f"Description pour {produit.nom}",
            quantite=1,  # Valeur par défaut, à ajuster si nécessaire
            montant=produit.prix_unitaire * 1  # Calcul simple du montant
        )
        ligne.save()  # Enregistrement de la ligne dans la base de données

def remplir_lignes_facture(request):
    # Exemple : Récupérer l'ID de la facture depuis les paramètres GET de la requête
    facture_id = request.GET.get("facture_id")
    
    if not facture_id:
        return HttpResponse("L'ID de la facture est requis.", status=400)

    try:
        # Vérifiez si la facture existe
        facture = Facture.objects.get(id=facture_id)
    except Facture.DoesNotExist:
        return HttpResponse("La facture spécifiée n'existe pas.", status=404)

    # Appelez la fonction creer_lignes_facture avec l'ID de la facture
    creer_lignes_facture(facture_id)
    return HttpResponse("Lignes de facture créées avec succès.")