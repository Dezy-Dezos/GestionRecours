from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JuryProfile
from structure.models import Domaine, Departement
from recours.models import Recours
from recours.forms import RecoursDecisionForm
from notifications.models import Notification

    

@login_required
def jury_dashboard(request):
    user = request.user

    # Vérifier que c'est bien un Jury
    if user.role != user.Roles.JURY:
        return redirect("dashboard_redirect")

    # Vérifier ou créer automatiquement le JuryProfile
    domaine_defaut = Domaine.objects.first()
    profile, created = JuryProfile.objects.get_or_create(
        user=user,
        defaults={"domaine": domaine_defaut, "fonction": "Membre"}
    )

    return render(request, "jury/home.html", {"profile": profile})


@login_required
def tous_les_recours(request):
    """Liste des recours du domaine du jury connecté, avec filtre par département"""
    user = request.user
    if not hasattr(user, "jury_profile"):
        messages.error(request, "Accès réservé aux jurys.")
        return redirect("dashboard_redirect")

    domaine = user.jury_profile.domaine
    departements = Departement.objects.filter(domaine=domaine)

    departement_id = request.GET.get("departement")
    recours = Recours.objects.filter(domaine=domaine).order_by("-date_envoi")
    if departement_id:
        recours = recours.filter(etudiant__departement_id=departement_id)

    return render(
        request,
        "jury/tous_les_recours.html",
        {
            "recours": recours,
            "departements": departements,
            "departement_id": departement_id,
        },
    )


@login_required
def traiter_recours(request, pk):
    """Le jury traite un recours et notifie l'étudiant"""
    user = request.user
    if not hasattr(user, "jury_profile"):
        messages.error(request, "Accès réservé aux jurys.")
        return redirect("dashboard_redirect")

    domaine = user.jury_profile.domaine
    recours = get_object_or_404(Recours, pk=pk, domaine=domaine)

    if request.method == "POST":
        form = RecoursDecisionForm(request.POST, instance=recours)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.jury_assigne = user.jury_profile
            rec.save()

            # 🔔 Notification à l’étudiant
            Notification.objects.create(
                user=rec.etudiant.user,
                message=f"⚖️ Votre recours '{rec.objet}' a été traité : {rec.get_statut_display()}"
            )

            messages.success(request, "✅ Décision enregistrée avec succès.")
            return redirect("tous_les_recours")
    else:
        form = RecoursDecisionForm(instance=recours)

    return render(request, "jury/traiter_recours.html", {"recours": recours, "form": form})


# ✅ detail d'un recours_JURY
@login_required
def detail_recours_jury(request, pk):
    user = request.user
    if user.role != user.Roles.JURY:
        messages.error(request, "Accès réservé au jury.")
        return redirect("dashboard_redirect")

    recours = get_object_or_404(Recours, pk=pk)
    return render(request, "jury/detail_recours.html", {"recours": recours})