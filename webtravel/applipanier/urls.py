from django.urls import path
from applipanier import views

urlpatterns = [
    path('panier/', views.afficherPanier, name='panier'),
    path('panier/add/<int:voyage_id>/', views.ajouterVoyageAuPanier, name='ajouter_au_panier'),
    path('panier/<int:voyage_id>/delete/', views.retirerDuPanier, name='retirer_du_panier'),
    path('panier/<int:voyage_id>/decrease/', views.retirerUnVoyageDuPanier, name='diminuer_quantite'),
    path('panier/delete/', views.viderPanier, name='vider_panier'),
    path('panier/pay/', views.payerPanier, name='payer_panier'),
    path('customers/', views.clients, name='clients'),
    path('allorders/', views.historiqueToutesCommandes, name='all_orders'),
    path('orders/<int:user_id>/', views.commandesParClient, name='commandes_client'),
    path('commandes/', views.historiqueCommandes, name='historique'),
    path('commandes/<int:commande_id>/', views.detailsCommande, name='details_commande'),
]