from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import EtudiantSignUpForm, JurySignUpForm
from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import User

# def home(request):
#     return render(request, "pages/home.html")

def accueil(request):
    return render(request, "pages/accueil.html")

def register_etudiant(request):
    if request.method == "POST":
        form = EtudiantSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription étudiant réussie !")
            return redirect("login")
    else:
        form = EtudiantSignUpForm()
    return render(request, "accounts/register_etudiant.html", {"form": form})


def register_jury(request):
    if request.method == "POST":
        form = JurySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription jury réussie !")
            return redirect("login")
    else:
        form = JurySignUpForm()
    return render(request, "accounts/register_jury.html", {"form": form})




def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection selon rôle
            if user.role == User.Roles.ETUDIANT:
                return redirect("etudiant_dashboard")
            elif user.role == User.Roles.JURY:
                return redirect("jury_dashboard")
            elif user.role == User.Roles.STAFF:
                return redirect("staff_dashboard")
            return redirect("dashboard_redirect")
        else:
            messages.error(request, "Identifiants incorrects. Réessayez.")
    else:
        form = CustomLoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == User.Roles.ETUDIANT:
        return redirect("etudiant_dashboard")
    elif user.role == User.Roles.JURY:
        return redirect("jury_dashboard")
    elif user.role == User.Roles.STAFF:
        return redirect("staff_dashboard")
    return redirect("login")


@login_required
def staff_dashboard(request):
    return render(request, "accounts/staff_home.html")



def logout_view(request):
    logout(request)
    return redirect('accueil')

