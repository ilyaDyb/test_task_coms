from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import PrivateOffice

User = get_user_model()

@receiver(post_save, sender=User)
def create_private_office(sender, instance, created, **kwargs):
    if created:
        PrivateOffice.objects.create(user=instance)