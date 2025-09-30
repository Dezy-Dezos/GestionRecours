from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.etudiant_dashboard, name="etudiant_dashboard"),
    
    # path('dashboard/', views.dashboard_etudiant, name='dashboard_etudiant'),
]
