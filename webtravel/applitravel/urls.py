from django.contrib import admin
from django.urls import path
from applitravel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('voyages/', views.voyages), # voyages provient de l
    path('villes/', views.villes),
    path('voyages/<int:voyage_id>', views.voyage),
    path('villes/add', views.formulaireCreationVille),
    path('villes/create/', views.CreerVille, name='creer_ville'),
    path('voyages/add', views.formulaireCreationVoyage),
    path('voyages/create/', views.CreerVoyage, name='creer_voyage'),
    path('voyages/<int:IDVoyage>/addVoyage', views.ajouterEtape),

    # Voyages  
    path('voyages/<int:voyage_id>/delete/', views.supprimerVoyage),
    path('voyages/<int:voyage_id>/update/', views.afficherFormulaireModificationVoyage),
    path('voyages/<int:voyage_id>/updated/', views.modifierVoyage),

    # Villes 
    path('villes/<int:ville_id>/delete/', views.supprimerVille),
    path('villes/<int:ville_id>/update/', views.afficherFormulaireModificationVille),
    path('villes/<int:ville_id>/updated/', views.modifierVille),

    # Etapes 
    path('voyages/<int:voyage_id>/deleteEtape/<int:etape_id>/', views.supprimerEtapeDansVoyage),
    path('voyages/<int:voyage_id>/updateEtape/<int:etape_id>/', views.afficherFormulaireModificationEtape),
    path('voyages/<int:voyage_id>/updatedEtape/<int:etape_id>/', views.modifierEtapeDansVoyage),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)