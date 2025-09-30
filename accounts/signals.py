from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Désormais, les profils Étudiant et Jury sont créés
    uniquement via leurs formulaires d'inscription respectifs.
    """
    if not created:
        return

    # Ici on ne fait rien de spécial, 
    # le formulaire d'inscription s'occupe de créer le profil correct.
    return
