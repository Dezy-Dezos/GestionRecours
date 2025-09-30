from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.jury_dashboard, name="jury_dashboard"),
    path("recours/", views.tous_les_recours, name="tous_les_recours"),
    path("recours/<int:pk>/", views.traiter_recours, name="traiter_recours"),
    
     path("recours/<int:pk>/detail/", views.detail_recours_jury, name="detail_recours_jury"),
    path("recours/<int:pk>/traiter/", views.traiter_recours, name="traiter_recours"),
]
