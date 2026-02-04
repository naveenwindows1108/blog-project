from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import CustomUser


# @receiver(post_save, sender=CustomUser)
# def user_created(sender, instance, created, **kwargs):
#     if created:
#         print('User created', instance.email)


read_signal = Signal(['date_time'])
