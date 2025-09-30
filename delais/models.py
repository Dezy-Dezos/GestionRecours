from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from structure.models import Domaine

class Delai(models.Model):
    domaine = models.ForeignKey(
        Domaine,
        on_delete=models.CASCADE,
        related_name='delais'
    )
    titre = models.CharField(max_length=200)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    actif = models.BooleanField(default=True, help_text="Décochez pour désactiver manuellement ce délai")

    class Meta:
        ordering = ["-date_debut"]

    def est_actif(self):
        now = timezone.now()
        return self.actif and self.date_debut <= now <= self.date_fin

    def clean(self):
        if self.date_debut >= self.date_fin:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

    def save(self, *args, **kwargs):
        if timezone.is_naive(self.date_debut):
            self.date_debut = timezone.make_aware(self.date_debut)
        if timezone.is_naive(self.date_fin):
            self.date_fin = timezone.make_aware(self.date_fin)
        super().save(*args, **kwargs)

    @classmethod
    def dernier_actif(cls, domaine):
        return cls.objects.filter(
            domaine=domaine,
            actif=True,
            date_debut__lte=timezone.now(),
            date_fin__gte=timezone.now()
        ).first()

    def __str__(self):
        return f"{self.titre} - {self.domaine.nom} [{self.date_debut:%d/%m/%Y %H:%M} → {self.date_fin:%d/%m/%Y %H:%M}]"
