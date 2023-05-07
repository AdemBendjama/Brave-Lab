from django.contrib.auth.models import  Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client

@receiver(post_save, sender=Client)
def add_client_to_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='client'))
