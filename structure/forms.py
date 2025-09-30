from django import forms
from .models import Domaine, Departement, Communique

class CommuniqueForm(forms.ModelForm):
    class Meta:
        model = Communique
        fields = ["titre", "contenu", "est_global", "domaine"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            if user.role == user.Roles.JURY:
                # Jury → pas de choix domaine ni global
                self.fields.pop("est_global")
                self.fields.pop("domaine")

            elif user.role == user.Roles.STAFF:
                # Staff → choix global ou domaine
                self.fields["domaine"].required = False
                
# class CommuniqueForm(forms.ModelForm):
#     class Meta:
#         model = Communique
#         fields = ["titre", "contenu", "est_global", "domaine"]
#         widgets = {
#             "contenu": forms.Textarea(attrs={"rows": 4}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         if user:
#             if user.role == user.Roles.JURY:
#                 # Jury ne peut pas choisir domaine ni publier global
#                 self.fields['domaine'].widget = forms.HiddenInput()
#                 self.fields['domaine'].initial = user.jury_profile.domaine
#                 self.fields['est_global'].widget = forms.HiddenInput()
#                 self.fields['est_global'].initial = False
        


class DomaineForm(forms.ModelForm):
    class Meta:
        model = Domaine
        fields = ["nom"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du domaine"
            })
        }

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ["domaine", "nom"]
        widgets = {
            "domaine": forms.Select(attrs={"class": "form-control"}),
            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du département"
            })
        }
        