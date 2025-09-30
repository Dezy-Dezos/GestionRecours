from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
    path("domaines/", views.liste_domaines, name="liste_domaines"),
    path("domaines/ajouter/", views.ajouter_domaine, name="ajouter_domaine"),
    path("domaines/modifier/<int:pk>/", views.modifier_domaine, name="modifier_domaine"),
    path("domaines/supprimer/<int:pk>/", views.supprimer_domaine, name="supprimer_domaine"),

    # Départements
    path("departements/", views.liste_departements, name="liste_departements"),
    path("departements/ajouter/", views.ajouter_departement, name="ajouter_departement"),
    path("departements/modifier/<int:pk>/", views.modifier_departement, name="modifier_departement"),
    path("departements/supprimer/<int:pk>/", views.supprimer_departement, name="supprimer_departement"),
    
    #communiques
     # Liste des communiqués
    path('communiques/', views.liste_communiques, name='liste_communiques'),

    # Ajouter un communiqué (STAFF & JURY)
    path('communiques/ajouter/', views.ajouter_communique, name='ajouter_communique'),

    # Modifier un communiqué
    path('communiques/modifier/<int:pk>/', views.modifier_communique, name='modifier_communique'),

    # Supprimer un communiqué
    path('communiques/supprimer/<int:pk>/', views.supprimer_communique, name='supprimer_communique'),

    # Détails d'un communiqué
    path('communiques/<int:pk>/', views.detail_communique, name='detail_communique'),

    # côté étudiant
    # path('etudiants/communiques/', views.liste_communiques_etudiant, name = 'liste_commun_etudiants')
]
