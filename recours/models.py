from django.db import models
from etudiants.models import EtudiantProfile
from jury.models import JuryProfile
from structure.models import Domaine

class Recours(models.Model):
    class Statut(models.TextChoices):
        ENVOYE = 'ENVOYE', 'Envoyé'
        EN_COURS = 'EN_COURS', 'En cours de traitement'
        ACCEPTE = 'ACCEPTE', 'Accepté'
        REJETE = 'REJETE', 'Rejeté'

    etudiant = models.ForeignKey(EtudiantProfile, on_delete=models.CASCADE, related_name='recours')
    domaine = models.ForeignKey(Domaine, on_delete=models.PROTECT, related_name='recours')
    jury_assigne = models.ForeignKey(JuryProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='recours_assignes')

    objet = models.CharField(max_length=255)
    message = models.TextField()
    fichier_joint = models.FileField(upload_to='recours_fichiers/', blank=True, null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ENVOYE)
    decision = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Recours #{self.pk} - {self.etudiant.user.get_full_name()}"
