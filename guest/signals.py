from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from guest.models import ProfilePic


@receiver(post_save, sender=User)
def create_profilepic(sender, instance, created, **kwargs):
    if created:
        ProfilePic.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profilepic(sender, instance, **kwargs):
        instance.profilepic.save()