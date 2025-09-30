from django import forms
from .models import Delai
from django.utils import timezone


class DelaiRecoursForm(forms.ModelForm):
    class Meta:
        model = Delai
        fields = ["titre", "date_debut", "date_fin"]
        widgets = {
            "date_debut": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "date_fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["date_debut", "date_fin"]:
            self.fields[field].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_date_debut(self):
        date_debut = self.cleaned_data["date_debut"]
        return timezone.make_aware(date_debut) if timezone.is_naive(date_debut) else date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data["date_fin"]
        return timezone.make_aware(date_fin) if timezone.is_naive(date_fin) else date_fin
