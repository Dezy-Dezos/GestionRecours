
from django.db import models
from django.conf import settings

class Domaine(models.Model):
    nom = models.CharField(max_length=200, unique=True)  # ex: Sciences et technologies

    def __str__(self):
        return self.nom

class Departement(models.Model):
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, related_name='departements')
    nom = models.CharField(max_length=200, unique=True)  # ex: Informatique, Aménagement...

    def __str__(self):
        return f"{self.nom} ({self.domaine.nom})"


#COMMUNIQUES #############

# models.py

class Communique(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domaine = models.ForeignKey("Domaine", on_delete=models.CASCADE, null=True, blank=True)
    est_global = models.BooleanField(default=False)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({'Global' if self.est_global else self.domaine})"
