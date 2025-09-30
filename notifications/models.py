# notifications/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notif({self.user.username}) - {self.message[:30]}"

