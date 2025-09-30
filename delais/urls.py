from django.urls import path
from . import views

urlpatterns = [
    path('delais/creer/', views.creer_delais, name='creer_delais'),
    path("modifier/<int:pk>/", views.modifier_delai, name="modifier_delai"),
    path("supprimer/<int:pk>/", views.supprimer_delai, name="supprimer_delai"),
]
