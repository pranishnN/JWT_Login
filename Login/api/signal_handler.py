# django
from django.db.models.signals import post_save
from django.dispatch import receiver

# app
from .models import masUser

@receiver(post_save, sender=masUser)
def user_update_handler(sender, instance, **kwargs):
    if instance.id:
        print('=======user_update_handler======', instance.otp)
        pass
    pass