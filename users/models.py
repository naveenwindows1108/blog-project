from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# class register(AbstractUser):
#     username = models.CharField(max_length=15)
#     password = models.CharField(max_length=12)
#     email = models.EmailField(unique=True)
#     firstname = models.CharField(blank=False)
#     lastname = models.CharField(blank=False)

#     def __str__(self):
#         return self.username


# table_name in database: users_Profile
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=10, unique=True)
    jwt_secret = models.CharField(max_length=64, editable=False)

    def save(self, *args, **kwargs):
        if not self.jwt_secret:
            self.jwt_secret = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
