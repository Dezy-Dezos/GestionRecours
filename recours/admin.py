from django.contrib import admin
from .models import Recours
@admin.register(Recours)
class RecoursAdmin(admin.ModelAdmin):
    list_display = ('id','etudiant','domaine','statut','date_envoi','jury_assigne')
    list_filter = ('statut','domaine','date_envoi')
    search_fields = ('objet','message','etudiant__user__username','etudiant__matricule')
