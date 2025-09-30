from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from delais.models import Delai
from notifications.models import *

@login_required
def etudiant_dashboard(request):
    user = request.user

    # Vérification que l'utilisateur est étudiant
    if not hasattr(user, "etudiant_profile") or user.role != user.Roles.ETUDIANT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("accueil")

    etu = user.etudiant_profile
    domaine = etu.departement.domaine

    # Récupérer le dernier délai actif
    now = timezone.now()
    delai_actif = Delai.objects.filter(
        domaine=domaine,
        date_debut__lte=now,
        date_fin__gte=now
    ).order_by("-date_debut").first()

    # Recours déjà soumis
    recours = etu.recours.order_by("-date_envoi")

    return render(request, "etudiants/dashboard.html", {
        "etudiant": etu,
        "delai_actif": delai_actif,
        "recours": recours,
    })


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

@login_required
def etudiant_dashboard(request):
    return render(request, "pages/home.html")
    notif_count = Notification.objects.filter(user=request.user, lu=False).count()
    return render(request, "etudiants/dashboard.html", {
        "notif_count": notif_count
    })
