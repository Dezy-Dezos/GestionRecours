from django import forms
from .models import Recours

class RecoursForm(forms.ModelForm):
    class Meta:
        model = Recours
        fields = ['objet', 'message', 'fichier_joint']


class RecoursDecisionForm(forms.ModelForm):
    class Meta:
        model = Recours
        fields = ["statut", "decision"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ⚠️ Limiter les statuts disponibles pour le jury
        self.fields["statut"].choices = [
            (Recours.Statut.EN_COURS, "En cours de traitement"),
            (Recours.Statut.ACCEPTE, "Accepté"),
            (Recours.Statut.REJETE, "Rejeté"),
        ]