from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from etudiants.models import EtudiantProfile
from jury.models import JuryProfile
from structure.models import Departement, Domaine

PROMO_CHOICES = [('L1','L1'), ('L2','L2'), ('L3','L3'), ('L4','L4')]

# ---- Formulaire Etudiant ----


class EtudiantSignUpForm(UserCreationForm):
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        label="Département"
    )
    promotion = forms.ChoiceField(
        choices=PROMO_CHOICES,
        label="Promotion"
    )
    photo_profil = forms.ImageField(
        label="Photo de profil",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'autre_nom', 'email', 'password1', 'password2')
        labels = {
            'username': 'Matricule',
            'first_name': 'Nom',
            'last_name': 'Post-nom',
            'autre_nom': 'prénom',
            'email': 'Adresse e-mail',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricule'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post-nom'}),
            'autre_nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer mot de passe'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.ETUDIANT
        if commit:
            user.save()
            EtudiantProfile.objects.create(
                user=user,
                departement=self.cleaned_data['departement'],
                promotion=self.cleaned_data['promotion'],
                photo_profil=self.cleaned_data.get('photo_profil')
            )
        return user


# ---- Formulaire Jury ----
class JurySignUpForm(UserCreationForm):
    domaine = forms.ModelChoiceField(queryset=Domaine.objects.all(), label="Domaine")
    fonction = forms.CharField(label="Fonction", max_length=150)
    # telephone = forms.CharField(label="Téléphone", max_length=20, required=False)
    photo_profil = forms.ImageField(label="Photo de profil",required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'autre_nom', 'email', 'password1', 'password2')
        labels = {
            'username': 'Identifiant',
            'first_name': 'Nom',
            'last_name': 'Post-nom',
            'autre_nom': 'Prénom',
            'email': 'Adresse e-mail',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricule'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post-nom'}),
            'autre_nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer mot de passe'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.JURY
        if commit:
            user.save()
            JuryProfile.objects.create(
                user=user,
                domaine=self.cleaned_data['domaine'],
                fonction=self.cleaned_data['fonction'],
                # telephone=self.cleaned_data.get('telephone'),
                photo_profil=self.cleaned_data.get('photo_profil')
            )
        return user




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Matricule",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Entrez votre matricule"})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Entrez votre mot de passe"})
    )

    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'autre_nom', 'email']
        labels = {
            'first_name': 'Nom',
            'last_name': 'Post-nom',
            'autre_nom': 'Prénom',
            'email': 'Adresse e-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post-nom'}),
            'autre_nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
                                             
