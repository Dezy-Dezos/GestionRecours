from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Colonnes visibles dans la liste
    list_display = ("username", "first_name", "last_name",  "autre_nom", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")

    # Champs éditables dans le formulaire admin
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "autre_nom", "email")}),
        ("Rôle", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Champs disponibles à la création d'un nouvel utilisateur
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "autre_nom", "email", "role", "password1", "password2"),
        }),
    )
