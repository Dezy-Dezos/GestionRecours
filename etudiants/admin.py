from django.contrib import admin
from .models import EtudiantProfile
@admin.register(EtudiantProfile)

class EtudiantAdmin(admin.ModelAdmin):
#     list_display = ('user', 'departement', 'promotion')
    search_fields = ('user__username',)
#     list_filter = ('departement', 'promotion')
