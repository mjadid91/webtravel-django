from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from applicompte.models import TravelUser
from applipanier.models import Commande, LigneCommande
from applitravel.models import Voyage
from datetime import date


def afficherPanier(request):
    user = None
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        # On récupère le panier (commande non payée)
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()

        if panier:
            lignes = LigneCommande.objects.filter(Commande_ID=panier)

            # Construction des détails pour le template
            lignes_panier = []
            total_global = 0

            for ligne in lignes:
                total_ligne = ligne.Prix * ligne.Quantite
                total_global += total_ligne

                lignes_panier.append({
                    'Voyage': ligne.Voyage_ID,
                    'Quantite': ligne.Quantite,
                    'PrixUnitaire': ligne.Prix,
                    'TotalLigne': total_ligne,
                    'IDVoyage': ligne.Voyage_ID.IDVoyage
                })

            # Mise à jour du prix total du panier pour être sûr
            panier.Prix = total_global
            panier.save()

            return render(request, 'applipanier/panier.html', {
                'user': user,
                'panier': panier,
                'lignes_panier': lignes_panier,
                'total_global': total_global
            })
        else:
            # Panier vide ou inexistant
            return render(request, 'applipanier/panier.html', {
                'user': user,
                'panier': None,
                'lignes_panier': [],
                'total_global': 0
            })
    else:
        return render(request, 'applicompte/login.html')


def ajouterVoyageAuPanier(request, voyage_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        voyage = Voyage.objects.get(IDVoyage=voyage_id)

        # Récupération ou création du panier
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()
        if not panier:
            panier = Commande()
            panier.User_ID = user
            panier.Payee = False
            panier.DateCommande = date.today()
            panier.Prix = 0
            panier.save()

        # Mise à jour du prix du panier (on ajoute le prix du voyage)
        panier.Prix += voyage.Prix
        panier.save()

        # Gestion de la ligne de commande
        ligne = LigneCommande.objects.filter(Commande_ID=panier, Voyage_ID=voyage).first()
        if ligne:
            ligne.Quantite += 1
            ligne.save()
        else:
            ligne = LigneCommande()
            ligne.Commande_ID = panier
            ligne.Voyage_ID = voyage
            ligne.Quantite = 1
            ligne.Prix = voyage.Prix
            ligne.save()

        return redirect('panier')  # Redirection vers la vue du panier
    else:
        return render(request, 'applicompte/login.html')


def retirerDuPanier(request, voyage_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()

        if panier:
            voyage = Voyage.objects.get(IDVoyage=voyage_id)
            ligne = LigneCommande.objects.filter(Commande_ID=panier, Voyage_ID=voyage).first()

            if ligne:
                # On retire le montant total de cette ligne du panier
                panier.Prix -= (ligne.Prix * ligne.Quantite)
                panier.save()
                ligne.delete()

            # Si le panier n'a plus de lignes, on peut le supprimer (optionnel, selon le TP)
            if not LigneCommande.objects.filter(Commande_ID=panier).exists():
                panier.delete()

        return redirect('panier')
    else:
        return render(request, 'applicompte/login.html')


def retirerUnVoyageDuPanier(request, voyage_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()

        if panier:
            voyage = Voyage.objects.get(IDVoyage=voyage_id)
            ligne = LigneCommande.objects.filter(Commande_ID=panier, Voyage_ID=voyage).first()

            if ligne:
                # On retire le prix d'une unité du panier
                panier.Prix -= ligne.Prix
                panier.save()

                if ligne.Quantite > 1:
                    ligne.Quantite -= 1
                    ligne.save()
                else:
                    # Si quantité tombe à 0, on supprime la ligne
                    ligne.delete()

            # Vérification panier vide
            if not LigneCommande.objects.filter(Commande_ID=panier).exists():
                panier.delete()

        return redirect('panier')
    else:
        return render(request, 'applicompte/login.html')


def viderPanier(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()

        if panier:
            panier.delete()  # La suppression en cascade effacera les lignes

        return redirect('panier')
    else:
        return render(request, 'applicompte/login.html')


def payerPanier(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        panier = Commande.objects.filter(User_ID=user, Payee=False).first()

        if panier:
            panier.Payee = True
            panier.save()
            return render(request, 'applipanier/avisPaiement.html', {'user': user, 'panier': panier})

        return redirect('panier')
    else:
        return render(request, 'applicompte/login.html')

def clients(request):
    if request.user.is_staff:
        lesClients = TravelUser.objects.filter(is_staff=False).order_by('date_joined')
        return render(
            request,
            'applipanier/clients.html',
            {'clients': lesClients, 'user': request.user}
        )
    else:
        return render(
            request,
            'applicompte/login.html'
        )
def historiqueToutesCommandes(request):
    if request.user.is_staff:
        # On récupère toutes les commandes payées, triées par date
        lesCommandesPayees = Commande.objects.filter(Payee=True).order_by('DateCommande')
        return render(request, 'applipanier/historiqueToutesCommandes.html', {'commandes': lesCommandesPayees, 'user': request.user})
    else:
        return render(request, 'applicompte/login.html')


def commandesParClient(request, user_id):
    if request.user.is_staff:
        client = TravelUser.objects.get(id=user_id)
        lesCommandes = Commande.objects.filter(User_ID=client, Payee=True).order_by('-DateCommande')

        return render(request, 'applipanier/commandes_client.html', {
            'commandes': lesCommandes,
            'user': request.user,
            'client_concerne': client  # On passe le client au template pour afficher son nom
        })
    else:
        return render(request, 'applicompte/login.html')


def historiqueCommandes(request):
    # Sécurité : accessible uniquement aux utilisateurs connectés
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        # On récupère uniquement les commandes payées de cet utilisateur
        lesCommandes = Commande.objects.filter(User_ID=user, Payee=True).order_by('-DateCommande')

        return render(request, 'applipanier/historiqueCommandes.html', {
            'user': user,
            'commandes': lesCommandes
        })
    else:
        return render(request, 'applicompte/login.html')


def detailsCommande(request, commande_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        # On récupère la commande en vérifiant qu'elle appartient bien à l'utilisateur (Sécurité !)
        try:
            laCommande = Commande.objects.get(IDCommande=commande_id, User_ID=user)
            lesLignes = LigneCommande.objects.filter(Commande_ID=laCommande)

            # Calcul du total pour vérification (optionnel si déjà stocké dans Prix)
            # Mais utile pour afficher le détail
            details = []
            for ligne in lesLignes:
                details.append({
                    'voyage': ligne.Voyage_ID,
                    'quantite': ligne.Quantite,
                    'prix_unitaire': ligne.Prix,
                    'total_ligne': ligne.Quantite * ligne.Prix
                })

            return render(request, 'applipanier/detailsCommande.html', {
                'user': user,
                'commande': laCommande,
                'lignes': details
            })

        except Commande.DoesNotExist:
            # Si l'utilisateur essaie d'accéder à une commande qui n'est pas la sienne
            return redirect('historique')

    else:
        return render(request, 'applicompte/login.html')