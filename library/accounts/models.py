from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    pass
    USER_TYPE_CHOICES = (
        (1, 'librarian'),
        (2, 'member'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    def __str__(self):
        return self.username