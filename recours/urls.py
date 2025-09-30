from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('recours/creer/', views.creer_recours, name='creer_recours'),
    path('recours/mes/', views.mes_recours, name='mes_recours'),
    # path("creer/", views.creer_recours, name="creer_recours"),
    # path("mes-recours/", views.mes_recours, name="mes_recours")
    
    
    path('recours/<int:pk>/modifier/', views.modifier_recours, name='modifier_recours'),
    path('recours/<int:pk>/supprimer/', views.supprimer_recours, name='supprimer_recours'),
    path("recours/<int:pk>/", views.detail_recours_etudiant, name="detail_recours_etudiant"),  # 👈 détail
    
]
