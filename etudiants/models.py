from django.db import models
from django.conf import settings
from structure.models import Departement

PROMO_CHOICES = [('L1','L1'), ('L2','L2'), ('L3','L3'), ('L4','L4')]

class EtudiantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='etudiant_profile'
    )
    departement = models.ForeignKey(
        Departement, 
        on_delete=models.PROTECT, 
        related_name='etudiants'
    )
    promotion = models.CharField(max_length=2, choices=PROMO_CHOICES)
    photo_profil = models.ImageField(upload_to='photos_etudiants/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.promotion} - {self.departement.nom}"
