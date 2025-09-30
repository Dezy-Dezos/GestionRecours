from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from notifications.models import Notification
from delais.models import Delai
from recours.models import Recours

# 🔔 Quand un délai est créé
@receiver(post_save, sender=Delai)
def notif_delai_defini(sender, instance, created, **kwargs):
    if created:
        # Tous les étudiants du domaine reçoivent une notif
        etudiants = instance.domaine.departements.all().values_list("etudiants__user", flat=True)
        for user_id in etudiants:
            if user_id:
                Notification.objects.create(
                    user_id=user_id,
                    message=f"📅 Un délai de recours a été défini : {instance.titre} "
                            f"({instance.date_debut.date()} → {instance.date_fin.date()})"
                )



# 🔔 Quand un recours est créé
@receiver(post_save, sender=Recours)
def notif_recours_envoye(sender, instance, created, **kwargs):
    if created:
        # Tous les jurys du domaine reçoivent une notif
        for jury in instance.domaine.jurys.all():
            Notification.objects.create(
                user=jury.user,
                message=f"📨 Un nouvel étudiant a envoyé un recours : {instance.objet}"
            )


# 🔔 Quand un recours est mis à jour (statut changé ou décision ajoutée)
@receiver(post_save, sender=Recours)
def notif_changement_statut(sender, instance, created, **kwargs):
    if not created:  # modification
        user = instance.etudiant.user
        Notification.objects.create(
            user=user,
            message=f"⚖️ Votre recours '{instance.objet}' est : {instance.get_statut_display()}"
        )
