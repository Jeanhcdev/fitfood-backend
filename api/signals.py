from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ClienteProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea o actualiza el perfil del usuario.
    """
    if created:
        ClienteProfile.objects.create(user=instance)
    instance.clienteprofile.save()