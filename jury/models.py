from django.db import models
from django.conf import settings
from structure.models import Domaine

class JuryProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jury_profile')
    domaine = models.ForeignKey(Domaine, on_delete=models.PROTECT, related_name='jurys')
    fonction = models.CharField(max_length=150, help_text="Ex: Président, Membre, Rapporteur")
    # telephone = models.CharField(max_length=20, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='photos_jurys/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.fonction} ({self.domaine.nom})"
