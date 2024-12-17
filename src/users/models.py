from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
