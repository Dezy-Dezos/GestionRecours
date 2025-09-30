from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Delai
from .forms import DelaiRecoursForm


# @login_required
# def creer_delais(request):
#     user = request.user

#     # Vérifier que c'est bien un jury
#     if user.role != user.Roles.JURY:
#         messages.error(request, "Seuls les jurys peuvent définir un délai.")
#         return redirect("dashboard_redirect")

#     # Vérifier que le jury a un profil
#     try:
#         jury = user.jury_profile
#     except Exception:
#         messages.error(request, "Aucun profil Jury associé à ce compte.")
#         return redirect("dashboard_redirect")

#     domaine = jury.domaine

#     # Vérification d’un délai existant encore valide
#     now = timezone.now()
#     delai_existant = Delai.objects.filter(
#         domaine=domaine,
#         date_fin__gte=now
#     ).order_by("-date_debut").first()

#     if request.method == "POST":
#         if delai_existant :
#             messages.error(request, "⛔ Impossible de créer un nouveau délai tant qu'un autre est actif ou programmé.")
#             return redirect("creer_delais")

#         form = DelaiRecoursForm(request.POST)
#         if form.is_valid():
#             delai = form.save(commit=False)
#             delai.domaine = domaine
#             delai.save()
#             messages.success(request, "✅ Délai ajouté avec succès.")
#             return redirect("jury_dashboard")
#     else:
#         form = DelaiRecoursForm()

#     # Récupération du dernier délai (pour chrono)
#     delais = Delai.objects.filter(domaine=domaine).order_by("-date_debut")
#     dernier_delai = delais.first()

#     return render(request, "delais/creer_delais.html", {
#         "form": form,
#         "delais": delais,
#         "dernier_delai": dernier_delai,
#         "delai_existant": delai_existant,  # 👉 envoyé au template
#     })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Delai
from .forms import DelaiRecoursForm

@login_required
def creer_delais(request):
    user = request.user

    # Vérifier que c'est bien un jury
    if user.role != user.Roles.JURY:
        messages.error(request, "Seuls les jurys peuvent définir un délai.")
        return redirect("dashboard_redirect")

    # Vérifier que le jury a un profil
    try:
        jury = user.jury_profile
    except Exception:
        messages.error(request, "Aucun profil Jury associé à ce compte.")
        return redirect("dashboard_redirect")

    domaine = jury.domaine

    if request.method == "POST":
        form = DelaiRecoursForm(request.POST)
        if form.is_valid():
            delai = form.save(commit=False)
            delai.domaine = domaine
            delai.save()
            messages.success(request, "✅ Délai ajouté avec succès.")
            return redirect("jury_dashboard")
    else:
        form = DelaiRecoursForm()

    # Récupération des délais du domaine (liste complète)
    delais = Delai.objects.filter(domaine=domaine).order_by("-date_debut")

    # Ne garder que le plus récent pour l’affichage
    dernier_delai = delais.first()

    return render(request, "delais/creer_delais.html", {
        "form": form,
        "delais": [dernier_delai] if dernier_delai else [],
        "dernier_delai": dernier_delai,
    })


# @login_required
# def creer_delais(request):
#     user = request.user

#     # Vérifier que c'est bien un jury
#     if user.role != user.Roles.JURY:
#         messages.error(request, "Seuls les jurys peuvent définir un délai.")
#         return redirect("dashboard_redirect")

#     # Vérifier que le jury a un profil
#     try:
#         jury = user.jury_profile
#     except Exception:
#         messages.error(request, "Aucun profil Jury associé à ce compte.")
#         return redirect("dashboard_redirect")

#     domaine = jury.domaine

#     if request.method == "POST":
#         form = DelaiRecoursForm(request.POST)
#         if form.is_valid():
#             delai = form.save(commit=False)
#             delai.domaine = domaine
#             delai.save()
#             messages.success(request, "✅ Délai ajouté avec succès.")
#             return redirect("jury_dashboard")
#     else:
#         form = DelaiRecoursForm()

#     # Récupération du dernier délai (pour chrono)
#     delais = Delai.objects.filter(domaine=domaine).order_by("-date_debut")
#     dernier_delai = delais.first()

#     return render(request, "delais/creer_delais.html", {
#         "form": form,
#         "delais": delais,
#         "dernier_delai": dernier_delai,
#     })
    
    


@login_required
def modifier_delai(request, pk):
    delai = get_object_or_404(Delai, pk=pk)

    if request.method == "POST":
        form = DelaiRecoursForm(request.POST, instance=delai)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Délai modifié avec succès.")
            return redirect("creer_delais")
    else:
        form = DelaiRecoursForm(instance=delai)

    return render(request, "delais/modifier_delai.html", {"form": form, "delai": delai})


@login_required
def supprimer_delai(request, pk):
    delai = get_object_or_404(Delai, pk=pk)
    delai.delete()
    messages.success(request, "🗑️ Délai supprimé avec succès.")
    return redirect("creer_delais")