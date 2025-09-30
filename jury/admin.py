from django.contrib import admin
from .models import JuryProfile
@admin.register(JuryProfile)
class JuryAdmin(admin.ModelAdmin):
    # list_display = ('user', 'domaine', 'fonction', 'telephone')
    list_display = ('user', 'domaine', 'fonction')
    list_filter = ('domaine',)
