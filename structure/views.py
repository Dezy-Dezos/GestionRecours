from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import DomaineForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CommuniqueForm
from .models import Communique
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Domaine, Departement
from .forms import DomaineForm, DepartementForm


# === Domaine ===
@login_required
def liste_domaines(request):
    domaines = Domaine.objects.all()
    return render(request, "admin/domaines/liste.html", {"domaines": domaines})

@login_required
def ajouter_domaine(request):
    if request.user.role != request.user.Roles.STAFF:
        messages.error(request, "⛔ Seul l'admin peut gérer les domaines.")
        return redirect("dashboard_redirect")
    
    if request.method == "POST":
        form = DomaineForm(request.POST)
        if form.is_valid():
            domaine = form.save()
            messages.success(request, f"✅ Domaine « {domaine.nom} » ajouté.")
            return redirect("liste_domaines")
    else:
        form = DomaineForm()
    return render(request, "admin/domaines/ajouter.html", {"form": form})

@login_required
def modifier_domaine(request, pk):
    domaine = get_object_or_404(Domaine, pk=pk)
    form = DomaineForm(request.POST or None, instance=domaine)
    if form.is_valid():
        form.save()
        messages.success(request, f"✏️ Domaine « {domaine.nom} » modifié.")
        return redirect("liste_domaines")
    return render(request, "admin/domaines/modifier.html", {"form": form})

@login_required
def supprimer_domaine(request, pk):
    domaine = get_object_or_404(Domaine, pk=pk)
    if request.method == "POST":
        domaine.delete()
        messages.success(request, "🗑️ Domaine supprimé.")
        return redirect("liste_domaines")
    return render(request, "admin/domaines/supprimer.html", {"domaine": domaine})


# === Département ===
@login_required
def liste_departements(request):
    departements = Departement.objects.select_related("domaine").all()
    return render(request, "admin/departements/liste.html", {"departements": departements})

@login_required
def ajouter_departement(request):
    if request.user.role != request.user.Roles.STAFF:
        messages.error(request, "⛔ Seul l'admin peut gérer les départements.")
        return redirect("dashboard_redirect")
    
    if request.method == "POST":
        form = DepartementForm(request.POST)
        if form.is_valid():
            departement = form.save()
            messages.success(request, f"✅ Département « {departement.nom} » ajouté.")
            return redirect("liste_departements")
    else:
        form = DepartementForm()
    return render(request, "admin/departements/ajouter.html", {"form": form})

@login_required
def modifier_departement(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    form = DepartementForm(request.POST or None, instance=departement)
    if form.is_valid():
        form.save()
        messages.success(request, f"✏️ Département « {departement.nom} » modifié.")
        return redirect("liste_departements")
    return render(request, "admin/departements/modifier.html", {"form": form})

@login_required
def supprimer_departement(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == "POST":
        departement.delete()
        messages.success(request, "🗑️ Département supprimé.")
        return redirect("liste_departements")
    return render(request, "admin/departements/supprimer.html", {"departement": departement})



# COMMINQUES

# @login_required
# def liste_communiques(request):
#     user = request.user  

#     # Cas STAFF
#     if user.role == user.Roles.STAFF:
#         communiques = Communique.objects.all().order_by("-date_publication")
#         base_template = "accounts/staff_dashboard.html"

#     # Cas JURY
#     elif user.role == user.Roles.JURY and hasattr(user, "jury_profile"):
#         jury = user.jury_profile
#         communiques = Communique.objects.filter(
#             models.Q(domaine=jury.domaine) | models.Q(domaine__isnull=True)
#         ).order_by("-date_publication")
#         base_template = "jury/base.html"

#     # Cas ETUDIANT
#     elif user.role == user.Roles.ETUDIANT and hasattr(user, "etudiant_profile"):
#         etudiant = user.etudiant_profile
#         communiques = Communique.objects.filter(
#             models.Q(domaine=etudiant.departement.domaine) | models.Q(domaine__isnull=True)
#         ).order_by("-date_publication")
#         base_template = "pages/base.html"

#     # Si aucun profil valide
#     else:
#         messages.error(request, "Profil non reconnu.")
#         return redirect("dashboard_redirect")

#     return render(
#         request,
#         "communiques/liste.html",
#         {
#             "communiques": communiques,
#             "base_template": base_template
#         }
#     )

# # @login_required
# # def liste_communiques(request):
# #     if request.user.role == request.user.Roles.STAFF:  # Admin → voit tout
# #         communiques = Communique.objects.all().order_by("-date_publication")
# #         base_template = "accounts/staff_dashboard.html"
# #     elif request.user.role == request.user.Roles.JURY:  # Jury → seulement son domaine
# #         communiques = Communique.objects.filter(domaine=request.user.jury_profile.domaine).order_by("-date_publication")
# #         base_template = "jury/base.html"
# #     else:  # Étudiant
# #         communiques = Communique.objects.filter(
# #             est_global=True
# #         ) | Communique.objects.filter(domaine=request.user.etudiant_profile.domaine)
# #         communiques = communiques.order_by("-date_publication")
# #         base_template = "pages/base.html"

# #     return render(request, "communiques/liste.html", {"communiques": communiques, "base_template": base_template})


# @login_required
# def ajouter_communique(request):
#     if request.user.role == request.user.Roles.STAFF:
#         base_template = "accounts/staff_dashboard.html"
#     elif request.user.role == request.user.Roles.JURY:
#         base_template = "jury/base.html"
#     else:
#         messages.error(request, "❌ Accès refusé.")
#         return redirect("dashboard_redirect")

#     if request.method == "POST":
#         form = CommuniqueForm(request.POST, request.FILES, user=request.user)
#         if form.is_valid():
#             communique = form.save(commit=False)
#             communique.auteur = request.user
#             # Pour le jury, on attribue automatiquement son domaine
#             if request.user.role == request.user.Roles.JURY:
#                 communique.domaine = request.user.jury_profile.domaine
#                 communique.est_global = False
#             communique.save()
#             messages.success(request, "✅ Communiqué ajouté avec succès.")
#             return redirect("liste_communiques")
#     else:
#         form = CommuniqueForm(user=request.user)

#     return render(request, "communiques/ajouter.html", {"form": form, "base_template": base_template})


# @login_required
# def modifier_communique(request, pk):
#     communique = get_object_or_404(Communique, pk=pk)
    
#     # Vérification des permissions
#     if not (request.user.role == request.user.Roles.STAFF or communique.auteur == request.user):
#         messages.error(request, "❌ Vous n'avez pas la permission de modifier ce communiqué.")
#         return redirect("liste_communiques")

#     if request.user.role == request.user.Roles.STAFF:
#         base_template = "accounts/staff_dashboard.html"
#     else:
#         base_template = "jury/base.html"

#     form = CommuniqueForm(request.POST or None, request.FILES or None, instance=communique, user=request.user)

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             messages.success(request, "✏️ Communiqué mis à jour.")
#             return redirect("liste_communiques")

#     return render(request, "communiques/modifier.html", {"form": form, "communique": communique, "base_template": base_template})


# @login_required
# def supprimer_communique(request, pk):
#     communique = get_object_or_404(Communique, pk=pk)

#     # Vérification des permissions
#     if not (request.user.role == request.user.Roles.STAFF or communique.auteur == request.user):
#         messages.error(request, "❌ Vous n'avez pas la permission de supprimer ce communiqué.")
#         return redirect("liste_communiques")

#     if request.user.role == request.user.Roles.STAFF:
#         base_template = "accounts/staff_dashboard.html"
#     else:
#         base_template = "jury/base.html"

#     if request.method == "POST":
#         communique.delete()
#         messages.success(request, "🗑️ Communiqué supprimé.")
#         return redirect("liste_communiques")

#     return render(request, "communiques/supprimer.html", {"communique": communique, "base_template": base_template})


# @login_required
# def detail_communique(request, pk):
#     communique = get_object_or_404(Communique, pk=pk)

#     if request.user.role == request.user.Roles.STAFF:
#         base_template = "accounts/staff_dashboard.html"
#     elif request.user.role == request.user.Roles.JURY:
#         base_template = "jury/base.html"
#     else:
#         base_template = "pages/base.html"

#     return render(request, "communiques/detail.html", {"communique": communique, "base_template": base_template})
# ## IIIIIIIIIIIIIIICCCCCCCCIIIIIIIIII ##

# @login_required
# def liste_communiques_etudiant(request):
#     user = request.user
#     if not hasattr(user, "etudiant_profile"):
#         messages.error(request, "Seuls les étudiants peuvent voir cette page.")
#         return redirect("dashboard_redirect")

#     etudiant = user.etudiant_profile
#     communiques = Communique.objects.filter(
#         models.Q(domaine=etudiant.departement.domaine) | models.Q(domaine__isnull=True)
#     ).order_by("-date_publication")

#     return render(request, "communiques/liste_etudiant.html", {"communiques": communiques})

def get_base_template(user):
    if user.role == user.Roles.STAFF:
        return "accounts/staff_dashboard.html"
    elif user.role == user.Roles.JURY:
        return "jury/base.html"
    else:
        return "pages/base.html"

#LISTE

@login_required
def liste_communiques(request):
    user = request.user

    # Récupération des communiqués selon le rôle
    if user.role == user.Roles.STAFF:
        communiques = Communique.objects.all().order_by("-date_publication")
    elif user.role == user.Roles.JURY:
        domaine = user.jury_profile.domaine
        communiques = Communique.objects.filter(est_global=True) | Communique.objects.filter(domaine=domaine)
        communiques = communiques.order_by("-date_publication")
    else:  # Étudiant
        domaine = user.etudiant_profile.departement.domaine
        communiques = Communique.objects.filter(est_global=True) | Communique.objects.filter(domaine=domaine)
        communiques = communiques.order_by("-date_publication")

    return render(request, "communiques/liste.html", {
        "communiques": communiques,
        "base_template": get_base_template(user),
    })
    
    #CREER

@login_required
def ajouter_communique(request):
    user = request.user
    if user.role not in [user.Roles.JURY, user.Roles.STAFF]:
        messages.error(request, "Vous n'avez pas la permission d'écrire un communiqué.")
        return redirect("dashboard_redirect")

    if request.method == "POST":
        form = CommuniqueForm(request.POST, user=user)
        if form.is_valid():
            communique = form.save(commit=False)
            communique.auteur = user

            if user.role == user.Roles.JURY:
                communique.est_global = False
                communique.domaine = user.jury_profile.domaine
            elif user.role == user.Roles.STAFF and communique.est_global:
                communique.domaine = None

            communique.save()
            messages.success(request, "✅ Communiqué publié avec succès.")
            return redirect("liste_communiques")
    else:
        form = CommuniqueForm(user=user)

    return render(request, "communiques/ajouter.html", {
        "form": form,
        "base_template": get_base_template(user),
    })

#DETAIL

@login_required
def detail_communique(request, pk):
    communique = get_object_or_404(Communique, pk=pk)
    return render(request, "communiques/detail.html", {
        "communique": communique,
        "base_template": get_base_template(request.user),
    })

#MODIFIER

@login_required
def modifier_communique(request, pk):
    communique = get_object_or_404(Communique, pk=pk)

    if request.user.role == request.user.Roles.JURY and communique.auteur != request.user:
        messages.error(request, "⛔ Vous ne pouvez modifier que vos propres communiqués.")
        return redirect("liste_communiques")

    if request.method == "POST":
        form = CommuniqueForm(request.POST, instance=communique, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Communiqué mis à jour avec succès.")
            return redirect("liste_communiques")
    else:
        form = CommuniqueForm(instance=communique, user=request.user)

    return render(request, "communiques/modifier.html", {
        "form": form,
        "communique": communique,
        "base_template": get_base_template(request.user),
    })


@login_required
def supprimer_communique(request, pk):
    communique = get_object_or_404(Communique, pk=pk)

    if request.user.role == request.user.Roles.JURY and communique.auteur != request.user:
        messages.error(request, "⛔ Vous ne pouvez supprimer que vos propres communiqués.")
        return redirect("liste_communiques")

    communique.delete()
    messages.success(request, "🗑️ Communiqué supprimé avec succès.")
    return redirect("liste_communiques")


