from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .manager import CustomUserManager
import datetime


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField()
    is_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=30,)

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = ['display_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
