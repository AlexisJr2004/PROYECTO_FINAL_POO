from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.core.models import Customer

from app.security.models import User

@receiver(post_save, sender=User)

def assign_user_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            print(instance)
            admin_group, created = Group.objects.get_or_create(name='Administradores')
            instance.groups.add(admin_group)
            Customer.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, dni=instance.dni, email=instance.email, phone=instance.phone)
        else:
            client_group, created = Group.objects.get_or_create(name='Clientes')
            instance.groups.add(client_group)
            Customer.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, dni=instance.dni, email=instance.email, phone=instance.phone)