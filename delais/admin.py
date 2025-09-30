from django.contrib import admin
from .models import Delai


@admin.register(Delai)
class DelaiRecoursAdmin(admin.ModelAdmin):
    list_display = ("titre", "domaine", "date_debut", "date_fin", "est_actif", "actif")
    list_filter = ("domaine", "date_debut", "date_fin", "actif")
    search_fields = ("titre", "domaine__nom")
    list_editable = ("actif",)
