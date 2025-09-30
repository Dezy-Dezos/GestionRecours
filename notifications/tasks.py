# notifications/tasks.py
from django.utils import timezone
from delais.models import Delai
from notifications.models import Notification

def notifier_delais_expirés():
    now = timezone.now()
    expirés = Delai.objects.filter(date_fin__lt=now, actif=True)

    for d in expirés:
        d.actif = False
        d.save()
        # Tous les étudiants du domaine reçoivent une notif
        etudiants = d.domaine.departements.all().values_list("etudiantprofile__user", flat=True)
        for user_id in etudiants:
            if user_id:
                Notification.objects.create(
                    user_id=user_id,
                    message=f"⛔ Le délai de recours '{d.titre}' est expiré."
                )
    return f"Notifié {expirés.count()} délais expirés."
# Peut être appelé périodiquement via un cron job ou un scheduler comme Celery