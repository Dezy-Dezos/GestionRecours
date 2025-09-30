from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("login/", views.login_view, name="login"),
    # path("home/", views.home, name="home"),
    path("register/etudiant/", views.register_etudiant, name="register_etudiant"),
    path("register/jury/", views.register_jury, name="register_jury"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("profile/", views.profile, name="profile"),
    # path("profile/edit/<int:id>/", views.profile, name="edit_profile"),
    path("redirect/", views.dashboard_redirect, name="dashboard_redirect")

]
