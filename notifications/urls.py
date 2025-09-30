# notifications/urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path("", views.mes_notifications, name="mes_notifications"),
]