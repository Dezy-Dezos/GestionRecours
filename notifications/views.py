from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def mes_notifications(request):
    notifications = request.user.notifications.order_by("-date_creation")

    # Choisir dynamiquement le bon base template
    if request.user.role == request.user.Roles.JURY:
        base_template = "jury/base.html"
    else:
        base_template = "pages/base.html"

    return render(request, "notifications/mes_notifications.html", {
        "notifications": notifications,
        "base_template": base_template,
    })
