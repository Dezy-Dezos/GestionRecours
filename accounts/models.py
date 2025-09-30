from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ETUDIANT = 'ETU', 'Étudiant'
        JURY = 'JUR', 'Jury'
        STAFF = 'STA', 'Staff/Administration'

    role = models.CharField(
        max_length=3,
        choices=Roles.choices,
        default=Roles.ETUDIANT,
        help_text="Rôle fonctionnel de l'utilisateur"
    )

    # Nouveau champ pour gérer les 3 noms
    autre_nom = models.CharField(
        max_length=150,
        help_text="Deuxième prénom ou deuxième nom selon la coutume"
    )

    def nom_complet(self):
        """
        Retourne l'identité complète : nom + prénom + autre nom
        """
        parts = [self.first_name, self.last_name,  self.autre_nom]
        return " ".join(p for p in parts if p)

    def __str__(self):
        return f"{self.username} - {self.nom_complet()}"
