from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from delais.models import *
from .forms import RecoursForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone  
from delais.models import Delai
from recours.models import *
from .forms import RecoursForm 


@login_required
def creer_recours(request):
    user = request.user
    if not hasattr(user, 'etudiant_profile'):
        messages.error(request, "Seuls les étudiants peuvent soumettre un recours.")
        return redirect('etudiant_dashboard')

    etu = user.etudiant_profile
    domaine = etu.departement.domaine

    # ⚠ Vérification du délai actif
    delais = Delai.objects.filter(domaine=domaine, actif=True)
    delai_actif = any(d.est_actif() for d in delais)
    # if not delai_actif:
    #     messages.error(request, "⛔ La période de recours est fermée pour votre domaine.")
    #     return redirect('etudiant_dashboard')

    if request.method == 'POST':
        form = RecoursForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.etudiant = etu
            rec.domaine = domaine
            rec.save()
            messages.success(request, "✅ Votre recours a été envoyé.")
            return redirect('mes_recours')
    else:
        form = RecoursForm()

    # On peut passer le dernier délai actif pour afficher le chrono
    delai = delais.order_by('-date_fin').first()

    return render(request, 'recours/rediger_recours.html', {
        'form': form,
        'delai': delai
    })
    
    

@login_required
def mes_recours(request):
    if not hasattr(request.user, 'etudiant_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('etudiant_dashboard')

    data = (
        request.user.etudiant_profile.recours
        .select_related('domaine')
        .order_by('-date_envoi')
    )
    return render(request, 'etudiants/mes_recours.html', {'recours': data})





# ✅ Modifier un recours
@login_required
def modifier_recours(request, pk):
    recours = get_object_or_404(Recours, pk=pk, etudiant=request.user.etudiant_profile)

    if recours.statut != Recours.Statut.ENVOYE:
        messages.error(request, "⛔ Impossible de modifier un recours déjà traité.")
        return redirect("mes_recours")

    if request.method == "POST":
        form = RecoursForm(request.POST, request.FILES, instance=recours)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Recours modifié avec succès.")
            return redirect("mes_recours")
    else:
        form = RecoursForm(instance=recours)

    return render(request, "recours/modifier_recours.html", {"form": form, "recours": recours})


# ✅ Supprimer un recours
@login_required
def supprimer_recours(request, pk):
    recours = get_object_or_404(Recours, pk=pk, etudiant=request.user.etudiant_profile)

    if recours.statut != Recours.Statut.ENVOYE:
        messages.error(request, "⛔ Impossible de supprimer un recours déjà traité.")
    else:
        recours.delete()
        messages.success(request, "🗑️ Recours supprimé avec succès.")

    return redirect("mes_recours")


#detail recours_ETUDIANT

@login_required
def detail_recours_etudiant(request, pk):
    user = request.user
    if user.role != user.Roles.ETUDIANT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("dashboard_redirect")

    recours = get_object_or_404(Recours, pk=pk, etudiant=user.etudiant_profile)
    return render(request, "recours/detail_recours.html", {"recours": recours})
